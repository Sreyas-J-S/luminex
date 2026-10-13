"""
Accounts views: register, login, logout, profile.
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ProfileUpdateForm


def register_view(request):
    """User registration."""
    if request.user.is_authenticated:
        return redirect('store:home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to Luminex, {user.first_name}! Your account has been created.")
            return redirect('store:home')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {
        'form': form,
        'page_title': 'Create Account | Luminex',
    })


def login_view(request):
    """User login."""
    if request.user.is_authenticated:
        return redirect('store:home')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next', '')
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            return redirect(next_url if next_url else 'store:home')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = LoginForm(request)

    return render(request, 'accounts/login.html', {
        'form': form,
        'page_title': 'Sign In | Luminex',
    })


def logout_view(request):
    """User logout (POST only for CSRF safety)."""
    if request.method == 'POST':
        logout(request)
        messages.info(request, "You have been signed out.")
    return redirect('store:home')


@login_required
def profile_view(request):
    """Protected user profile page."""
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect('accounts:profile')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileUpdateForm(instance=request.user)

    orders = request.user.orders.all()
    return render(request, 'accounts/profile.html', {
        'form': form,
        'orders': orders,
        'page_title': 'My Account | Luminex',
    })

