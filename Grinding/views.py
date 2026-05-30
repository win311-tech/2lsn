from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .forms import SignUpForm, LoginForm

from google.oauth2 import id_token
from google.auth.transport import requests

User = get_user_model()


def Index(request):
    """Public homepage - accessible to everyone"""
    return render(request, 'Index.html', {
        'user': request.user
    })


def Register(request):
    """Handle user registration"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in after signup
            login(request, user)
            messages.success(request, f'Welcome to 2LSN, {user.first_name}!')
            # Redirect to user dashboard (NOT admin)
            return redirect('dashboard')
        else:
            # Show errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = SignUpForm()

    return render(request, 'Register.html', {
        'form': form,
        'google_oauth_client_id': settings.GOOGLE_OAUTH_CLIENT_ID,
    })

def Login(request):
    """Handle user login"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        # form field names from Login.html are: email, password
        username = request.POST.get('email')
        password = request.POST.get('password')

        # Try to authenticate (username is stored as email in SignUpForm.save)
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            # Redirect to user dashboard (NOT admin)
            next_url = request.POST.get('next') or request.GET.get('next')
            # Always redirect to the dashboard unless a valid next is explicitly provided
            return redirect(next_url or 'dashboard')

        else:
            messages.error(request, 'Invalid email or password. Please try again.')

    form = LoginForm()
    return render(request, 'Login.html', {
        'form': form,
        'google_oauth_client_id': settings.GOOGLE_OAUTH_CLIENT_ID,
        'google_login_uri': request.build_absolute_uri(reverse('auth_receiver'))
    })




@csrf_exempt
def auth_receiver(request):
    if request.method != 'POST':
        return HttpResponse(status=405)

    token = request.POST.get('credential')
    if not token:
        return HttpResponse('Missing credential token', status=400)

    client_id = settings.GOOGLE_OAUTH_CLIENT_ID
    if not client_id:
        return HttpResponse('Google OAuth client ID is not configured.', status=500)

    try:
        user_data = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            client_id
        )
    except ValueError:
        return HttpResponse('Invalid Google token.', status=403)

    email = user_data.get('email')
    if not email:
        return HttpResponse('Google account did not provide an email address.', status=400)

    user = User.objects.filter(username__iexact=email).first() or User.objects.filter(email__iexact=email).first()
    if user is None:
        user = User.objects.create_user(username=email, email=email)
        user.first_name = user_data.get('given_name', '')
        user.last_name = user_data.get('family_name', '')
        user.set_unusable_password()
        user.save()
    elif user.username.lower() != email.lower():
        user.username = email
        user.save(update_fields=['username'])

    login(request, user)
    return redirect('dashboard')


def logout_view(request):
    """Handle user logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('index')


@login_required(login_url='login')
def dashboard_view(request):
    """User dashboard - only for logged-in users"""
    return render(request, 'dashboard.html', {
        'user': request.user
    })


def Shop(request):
    return render(request, 'Shop.html', {
        'user': request.user
    })


def About(request):
    return render(request, 'About.html', {
        'user': request.user
    })

@login_required(login_url='login')
def checkout(request):
    return render(request, 'checkout.html', {
        'user': request.user
    })

