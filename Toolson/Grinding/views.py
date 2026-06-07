from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .forms import SignUpForm, LoginForm
import os
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests


def redirect_localhost(request):
    host = request.get_host()
    if host.startswith('127.0.0.1'):
        parts = host.split(':', 1)
        port = parts[1] if len(parts) > 1 else ''
        new_host = f'localhost:{port}' if port else 'localhost'
        return request.build_absolute_uri(request.get_full_path()).replace(host, new_host, 1)
    return None


def Index(request):
    """Public homepage - accessible to everyone"""
    return render(request, 'index.html', {

        'user': request.user
    })


def Register(request):
    """Handle user registration"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    redirect_url = redirect_localhost(request)
    if redirect_url:
        return redirect(redirect_url)

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

    redirect_url = redirect_localhost(request)
    if redirect_url:
        return redirect(redirect_url)

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
    })



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



@csrf_exempt
def sign_in(request):
    return render(request, 'sign_in.html')
 
def auth_receiver(request):
    """Google Identity sends the credential to this endpoint."""

    token = request.POST.get('credential')
    if not token:
        return HttpResponse('Missing Google credential.', status=400)

    client_id = settings.GOOGLE_OAUTH_CLIENT_ID or os.environ.get('GOOGLE_OAUTH_CLIENT_ID')
    if not client_id:
        return HttpResponse('Google OAuth client ID is not configured.', status=500)

    try:
        user_data = id_token.verify_oauth2_token(
            token, requests.Request(), client_id
        )
    except ValueError as e:
        return HttpResponse(f'Invalid Google token: {e}', status=403)


    email = user_data.get('email')
    if not email:
        return HttpResponse('Google account did not provide an email address.', status=400)

    User = get_user_model()
    user, created = User.objects.get_or_create(
        username=email,
        defaults={
            'email': email,
            'first_name': user_data.get('given_name', ''),
            'last_name': user_data.get('family_name', ''),
        }
    )

    if created:
        user.set_unusable_password()
        user.save()

    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)
    return redirect('dashboard')


def sign_out(request):
    request.session.pop('user_data', None)
    return redirect('login')
 