from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .forms import SignUpForm, LoginForm
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests
import uuid
from django.urls import reverse
from .paystack import checkout
import hmac
import hashlib
import json
from .models import Product, OrderHistory


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
            login(request, user)
            messages.success(request, f'Welcome to 2LSN, {user.first_name}!')
            return redirect('dashboard')
        else:
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
        username = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            next_url = request.POST.get('next') or request.GET.get('next')
            return redirect(next_url or 'dashboard')

        messages.error(request, 'Invalid email or password. Please try again.')

    form = LoginForm()
    return render(request, 'Login.html', {
        'form': form,
        'google_oauth_client_id': settings.GOOGLE_OAUTH_CLIENT_ID,
        'login_template_id': 'toolson-template-login',
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


def sign_out(request):
    request.session.pop('user_data', None)
    return redirect('login')


@csrf_exempt
def auth_receiver(request):
    """Receive Google Identity Services (GSI) credential JWT and log the user in."""
    if request.method != 'POST':
        return HttpResponse(status=405)

    credential = request.POST.get('credential')
    if not credential:
        return HttpResponse(status=400)

    try:
        client_id = settings.GOOGLE_OAUTH_CLIENT_ID
        idinfo = id_token.verify_oauth2_token(
            credential,
            requests.Request(),
            client_id,
        )

        email = idinfo.get('email')
        if not email:
            return HttpResponse(status=400)

        UserModel = get_user_model()
        user, _created = UserModel.objects.get_or_create(
            email__iexact=email,
            defaults={'email': email, 'username': email},
        )

        if getattr(user, 'username', '') != email:
            user.username = email
        if not getattr(user, 'email', ''):
            user.email = email
        user.save()

        login(request, user)
        # Prevent unwanted redirect right after auth_receiver succeeds.
        # Frontend can decide what to do next.
        return HttpResponse(status=204)


    except Exception:
        return HttpResponse(status=401)
    
@login_required
def create_paystack_checkout_session(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    purchase_id = f"purchase_{uuid.uuid4()}"

    # Redirect back to the dashboard upon successful payment
    payment_success_url = reverse('dashboard')
    callback_url = f"{request.scheme}://{request.get_host()}{payment_success_url}"

    checkout_data = {
        "email": request.user.email,
        "amount": int(product.price * 100),  # in kobo (e.g. 2500 for NGN 25.00)
        "currency": "NGN",
        "channels": ["card", "bank_transfer", "bank", "ussd", "qr", "mobile_money"],
        "reference": purchase_id,
        "callback_url": callback_url,
        "metadata": {
            "product_id": product_id,
            "user_id": request.user.id,
            "Orderhistory_id": purchase_id,
        },
        "label": f"Checkout For {product.name}"
    }

    status, check_out_session_url_or_error_message = checkout(checkout_data)

    if status:
        return redirect(check_out_session_url_or_error_message)
    else:
        messages.error(request, check_out_session_url_or_error_message)
        return redirect('checkout')


@csrf_exempt 
def paystack_webhook(request):
    secret = settings.PAYSTACK_SECRET_KEY
    request_body = request.body

    hash = hmac.new(secret.encode('utf-8'), request_body, hashlib.sha512).hexdigest()
    
    if hash == request.META.get('HTTP_X_PAYSTACK_SIGNATURE'):
        webhook_post_data = json.loads(request_body)
        print(webhook_post_data)

        if webhook_post_data.get("event") == "charge.success":
            metadata = webhook_post_data["data"]["metadata"]

            product_id = metadata["product_id"]
            user_id = metadata["user_id"]
            Orderhistory_id = metadata["Orderhistory_id"]

            user_model = get_user_model()
            try:
                user = user_model.objects.get(id=user_id)
                OrderHistory.objects.create(
                    Orderhistory_id=Orderhistory_id,
                    user=user,
                    purchase_status=True
                )
            except user_model.DoesNotExist:
                pass

    return HttpResponse(status=200)

