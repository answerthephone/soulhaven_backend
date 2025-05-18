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
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def user_register(request):
    """
    API endpoint to register a new user.

    Expected JSON:
    {
        "username": "",
        "email": "",
        "password": "",
        "confirm_password": ""
    }

    Returns:
    - 201: Successful registration
    - 400: Validation or logic error
    - 409: Conflict (duplicate username/email)
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)

    try:
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if not all([username, email, password, confirm_password]):
            return JsonResponse({'error': 'All fields are required'}, status=400)

        if password != confirm_password:
            return JsonResponse({'error': 'Passwords do not match'}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already taken'}, status=409)

        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email already registered'}, status=409)

        User.objects.create_user(username=username, email=email, password=password)

        return JsonResponse({'message': 'Registration successful'}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

@csrf_exempt
def user_login(request):
    """
    API endpoint to authenticate and log in a user.

    Expected JSON:
    {
        "username": "",
        "password": ""
    }

    Returns:
    - 200: Success with user info
    - 401: Invalid credentials
    - 400: Bad request
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)

    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return JsonResponse({'error': 'Username and password are required'}, status=400)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Login successful'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)


@csrf_exempt
def user_logout(request):
    """
    API endpoint to log the user out.

    - Clears the session.
    - Returns a success message in JSON.

    Method: POST
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)

    logout(request)
    return JsonResponse({'message': 'Successfully logged out'}, status=200)


@login_required
def personal_account_view(request):
    """
    API endpoint to return user's personal account data.

    - Requires authentication.
    - Returns profile fields and basic user info.

    Method: GET
    """
    user = request.user
    profile = get_object_or_404(UserProfile, user=user)

    return JsonResponse({
        'username': user.username,
        'email': user.email,
        'nickname': profile.nickname,
        'level': profile.level,
        'stars': profile.stars,
        'avatar': profile.avatar.url if profile.avatar else None,
        'log_ins': profile.log_ins,
    })


@login_required
def profile_view(request):
    """
    API endpoint to return the authenticated user's profile data.

    - Requires user login.
    - Returns profile fields and user metadata.

    Method: GET
    """
    user = request.user
    profile = get_object_or_404(UserProfile, user=user)

    return JsonResponse({
        'username': user.username,
        'email': user.email,
        'nickname': profile.nickname,
        'age': profile.age,
        'level': profile.level,
        'stars': profile.stars,
        'avatar': profile.avatar.url if profile.avatar else None,
        'log_ins': profile.log_ins,
    })

@login_required
def calendar_view(request):
    """
    API endpoint to return user's login activity for calendar display.

    - Requires authentication.
    - Returns list of login dates (as ISO strings).

    Method: GET
    """
    profile = get_object_or_404(UserProfile, user=request.user)

    return JsonResponse({
        'log_ins': profile.log_ins or []
    })


@login_required
def star_history_view(request):
    """
    API endpoint to return user's star earning history.

    - Requires login.
    - Returns a list of actions with timestamps and amount of stars.

    Method: GET
    """
    history = StarHistory.objects.filter(user=request.user).select_related('action').order_by('-earned_at')

    return JsonResponse({
        'history': [
            {
                'action': entry.action.name,
                'amount': entry.action.amount,
                'earned_at': entry.earned_at.isoformat()
            }
            for entry in history
        ]
    })


@login_required
def user_achievements(request):
    """
    API endpoint to return user's unlocked achievements.

    - Requires login.
    - Returns name, description, image, and awarded time for each achievement.

    Method: GET
    """
    achievements = UserAchievement.objects.filter(user=request.user).select_related('achievement')

    return JsonResponse({
        'achievements': [
            {
                'name': ua.achievement.name,
                'description': ua.achievement.description,
                'image': ua.achievement.image.url if ua.achievement.image else None,
                'awarded_at': ua.awarded_at.isoformat()
            }
            for ua in achievements
        ]
    })


@csrf_exempt
@login_required
def edit_profile(request):
    """
    API endpoint to update user profile info.

    Expected JSON (any subset of):
    {
        "email": "newemail@example.com",
        "nickname": "NewNickname",
        "age": 25
    }

    Returns:
    - 200 on success
    - 400 if invalid input
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)

    user = request.user
    profile = UserProfile.objects.get(user=user)

    try:
        if request.content_type == "application/json":
            data = json.loads(request.body)
        else:
            data = request.POST

        email = data.get('email')
        if email:
            user.email = email
            user.save()

        nickname = data.get('nickname')
        age = data.get('age')

        if nickname:
            profile.nickname = nickname
        if age is not None:
            try:
                profile.age = int(age)
            except ValueError:
                return JsonResponse({'error': 'Age must be a number'}, status=400)

        profile.save()

        return JsonResponse({'message': 'Profile updated successfully'}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)