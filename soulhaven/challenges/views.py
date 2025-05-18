from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib import messages
from datetime import datetime, timedelta
from .models import Challenge, UserChallenge, ChallengeType
from challenges.logic import check_course_challenges, check_game_challenges
from courses.models import Course
from achievements.utils import award_achievement


@login_required
def challenge_detail_api(request, challenge_id):
    """
    API view to return detailed challenge info for the authenticated user.
    """
    challenge = get_object_or_404(Challenge, id=challenge_id)
    user_challenge, _ = UserChallenge.objects.get_or_create(user=request.user, challenge=challenge)

    return JsonResponse({
        'id': challenge.id,
        'name': challenge.name,
        'description': challenge.description,
        'type': challenge.type,
        'target_value': challenge.target_value,
        'star_reward': challenge.star_reward,
        'course_title': challenge.course_title,
        'active': challenge.active,
        'user_progress': {
            'progress': user_challenge.progress,
            'completed': user_challenge.completed,
            'completed_at': user_challenge.completed_at.isoformat() if user_challenge.completed_at else None
        }
    })


@csrf_exempt
@login_required
def complete_challenge_api(request, challenge_id):
    """
    API view to manually trigger a challenge completion check.

    Returns:
    - JSON response with success/failure status and any unlocked achievements.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    challenge = get_object_or_404(Challenge, id=challenge_id)
    user = request.user
    user_challenge, _ = UserChallenge.objects.get_or_create(user=user, challenge=challenge)

    unlocked = []

    if user_challenge.completed:
        return JsonResponse({'message': 'Challenge already completed'}, status=200)

    # Evaluate challenge type
    if challenge.type == ChallengeType.FINISH_COURSES:
        course = None
        if challenge.target_value == 1 and challenge.course_title:
            from courses.models import Course
            course = Course.objects.filter(title=challenge.course_title).first()
        check_course_challenges(user, course)

    elif challenge.type == ChallengeType.FINISH_GAMES:
        check_game_challenges(user, challenge.course_title)

    user_challenge.refresh_from_db()

    if user_challenge.completed:
        total_completed = UserChallenge.objects.filter(user=user, completed=True).count()

        # Achievements
        if total_completed == 1:
            if award_achievement(user, "First Challenge Completed", "You completed your first challenge!", "achievements/first_challenge.png"):
                unlocked.append({"name": "First Challenge Completed", "description": "You completed your first challenge!", "image": "achievements/first_challenge.png"})

        if total_completed == 3:
            if award_achievement(user, "Challenge Streak", "You’ve completed 3 challenges. Keep it up!", "achievements/challenge_streak.png"):
                unlocked.append({"name": "Challenge Streak", "description": "You’ve completed 3 challenges. Keep it up!", "image": "achievements/challenge_streak.png"})

        if total_completed == 10:
            if award_achievement(user, "Challenge Master", "You’ve completed 10 challenges — you're unstoppable!", "achievements/challenge_master.png"):
                unlocked.append({"name": "Challenge Master", "description": "You’ve completed 10 challenges — you're unstoppable!", "image": "achievements/challenge_master.png"})

        # Weekly Completionist
        start_of_week = datetime.today() - timedelta(days=datetime.today().weekday())
        weekly_challenges = Challenge.objects.filter(active=True, created_at__gte=start_of_week)
        completed_this_week = UserChallenge.objects.filter(user=user, challenge__in=weekly_challenges, completed=True).count()

        if weekly_challenges.exists() and completed_this_week == weekly_challenges.count():
            if award_achievement(user, "Weekly Completionist", "You've completed all challenges of the week!", "achievements/weekly_completionist.png"):
                unlocked.append({"name": "Weekly Completionist", "description": "You've completed all challenges of the week!", "image": "achievements/weekly_completionist.png"})

        # 14-Day Consistency
        streak_days = 14
        today = datetime.today().date()
        streak_dates = [today - timedelta(days=i) for i in range(streak_days)]

        has_streak = all(UserChallenge.objects.filter(user=user, completed=True, completed_at__date=day).exists() for day in streak_dates)

        if has_streak:
            if award_achievement(user, "Challenge Consistency", "You completed a challenge every day for 14 days!", "achievements/consistency_14.png"):
                unlocked.append({"name": "Challenge Consistency", "description": "You completed a challenge every day for 14 days!", "image": "achievements/consistency_14.png"})

        return JsonResponse({
            'status': 'completed',
            'message': f"Challenge '{challenge.name}' completed!",
            'achievements': unlocked
        })

    else:
        return JsonResponse({
            'status': 'incomplete',
            'message': 'You have not yet met the challenge requirements.'
        }, status=200)