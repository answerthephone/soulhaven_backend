from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserEditForm, ProfileEditForm
from .models import UserProfile
from accounts.decorators import with_star_history
from stars.models import StarHistory
from achievements.models import UserAchievement


def user_register(request):
    """
    Handles user registration.

    - Checks if the username or email already exists.
    - Creates a new user if valid.
    - Redirects to login page upon successful registration.
    """
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already taken")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already registered")
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                messages.success(request, "Registration successful! You can now log in.")
                return redirect('user_login')
        else:
            messages.error(request, "Passwords do not match")

    return render(request, 'register.html')


def user_login(request):
    """
    Handles user authentication (login).

    - Authenticates user credentials.
    - Redirects to homepage if login is successful.
    - Displays error message if credentials are invalid.
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('/')
        else:
            messages.error(request, "Invalid credentials")

    return render(request, 'login.html')


def user_logout(request):
    """
    Logs the user out and redirects to login page.

    - Clears the session.
    - Displays a logout success message.
    """
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('user_login')


@login_required
@with_star_history
def personal_account_view(request):
    """
    Displays the personal account page.

    - Requires user login.
    - Shows user profile information.
    - Provides access to personal account dashboard.
    """
    user = request.user
    profile = get_object_or_404(UserProfile, user=user)

    return render(request, 'accounts/personal_account.html', {
        'user': user,
        'profile': profile,
    })


@login_required
@with_star_history
def profile_view(request):
    """
    Displays the user's public profile page.

    - Requires user login.
    - Fetches and shows profile details.
    """
    user = request.user
    profile = get_object_or_404(UserProfile, user=user)

    return render(request, 'accounts/profile.html', {
        'user': user,
        'profile': profile,
    })


@login_required
@with_star_history
def calendar_view(request):
    """
    Displays the user's calendar page.

    - Requires user login.
    - Shows data like login streaks or activity history (if available).
    """
    user = request.user
    profile = get_object_or_404(UserProfile, user=user)

    return render(request, 'accounts/calendar.html', {
        'user': user,
        'profile': profile,
    })


@login_required
@with_star_history
def star_history_view(request):
    """
    Displays the user's star history.

    - Lists all star actions in reverse chronological order.
    - Requires user login.
    """
    history = StarHistory.objects.filter(user=request.user).select_related('action').order_by('-earned_at')
    return render(request, 'accounts/star_history.html', {'history': history})


@login_required
@with_star_history
def user_achievements(request):
    """
    Displays the user's achievements.

    - Requires user login.
    - Lists all achievements unlocked by the user.
    """
    achievements = UserAchievement.objects.filter(user=request.user).select_related('achievement')
    return render(request, 'accounts/user_achievements.html', {'achievements': achievements})


@login_required
def edit_profile(request):
    """
    Allows the user to edit their profile information.

    - Requires user login.
    - Displays and processes the user and profile update forms.
    - Redirects to profile page after successful update.
    """
    user = request.user
    profile = UserProfile.objects.get(user=user)

    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=user)
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserEditForm(instance=user)
        profile_form = ProfileEditForm(instance=profile)

    return render(request, 'accounts/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })