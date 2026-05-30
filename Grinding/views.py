from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm, LoginForm


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

    return render(request, 'Register.html', {'form': form})

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
    return render(request, 'Login.html', {'form': form})



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

