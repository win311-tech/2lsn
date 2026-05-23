from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm, LoginForm


def Index(request):
    """Public homepage - accessible to everyone"""
    return render(request, 'index.html', {
        'user': request.user
    })


def Register(request):
    """Handle user registration"""
    if request.user.is_authenticated:
        return redirect('Index')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in after signup
            login(request, user)
            messages.success(request, f'Welcome to Tasty Foods, {user.first_name}!')
            # Redirect to user dashboard (NOT admin)
            return redirect('Index')
        else:
            # Show errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = SignUpForm()

<<<<<<< HEAD
    return render(request, 'Register.html', {'form': form})

=======
    return render(request, 'register.html', {'form': form})
>>>>>>> e9c0c02 (Your commit message)

def Login(request):
    """Handle user login"""
    if request.user.is_authenticated:
        return redirect('Index')

    if request.method == 'POST':
        # Get username (email) and password from form
        username = request.POST.get('email')
        password = request.POST.get('password')

        # Try to authenticate
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            # Redirect to user dashboard (NOT admin)
            next_url = request.GET.get('next', 'Index')
            return redirect(next_url)
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
    return render(request, 'Index.html', {
        'user': request.user
    })

def Shop(request):

    return render(request, 'Shop.html', {
        'user': request.user
    })


def About(request):
    return render(request, 'about.html', {
        'user': request.user
    })

