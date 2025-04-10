from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Challenge, UserChallenge, ChallengeType
from challenges.logic import check_course_challenges, check_game_challenges
from courses.models import Course
from achievements.utils import award_achievement


@login_required
def challenge_detail(request, challenge_id):
    challenge = get_object_or_404(Challenge, id=challenge_id)
    user_challenge, created = UserChallenge.objects.get_or_create(user=request.user, challenge=challenge)

    if request.method == 'POST':
        if not user_challenge.completed:
            user_challenge.progress = 0
            user_challenge.save()
        return redirect('challenge_detail', challenge.id)

    return render(request, 'challenges/challenge_detail.html', {
        'challenge': challenge,
        'user_challenge': user_challenge
    })


@login_required
def complete_challenge(request, challenge_id):
    """
    View that processes the completion of a challenge by the user.

    Behavior:
    - Fetches the target challenge and the related UserChallenge record.
    - If already completed, notifies the user.
    - Otherwise, verifies progress based on challenge type (course/game).
    - Awards stars and unlocks achievements if criteria are met.

    Supported Achievements:
    - First Challenge Completed
    - Challenge Streak (3 challenges)
    - Challenge Master (10 challenges)
    - Weekly Completionist (all weekly challenges)
    - Challenge Consistency (1 challenge/day for 14 consecutive days)

    Session:
    - Stores `just_unlocked_achievements` in session for frontend popups.

    Redirects:
    - Always redirects to 'challenge_detail' page for the selected challenge.
    """
    challenge = get_object_or_404(Challenge, id=challenge_id)
    user_challenge, _ = UserChallenge.objects.get_or_create(user=request.user, challenge=challenge)

    unlocked = []

    if user_challenge.completed:
        messages.info(request, "Вы уже завершили этот челлендж.")
        return redirect('challenge_detail', challenge.id)

    if challenge.type == ChallengeType.FINISH_COURSES:
        from challenges.logic import check_course_challenges
        course_title = challenge.course_title if challenge.target_value == 1 else None
        course = None
        if course_title:
            from courses.models import Course
            course = Course.objects.filter(title=course_title).first()
        check_course_challenges(request.user, course)

    elif challenge.type == ChallengeType.FINISH_GAMES:
        from challenges.logic import check_game_challenges
        check_game_challenges(request.user, challenge.course_title)


    user_challenge.refresh_from_db()

    if user_challenge.completed:
        messages.success(request, f"Поздравляем! Вы завершили челлендж и получили {challenge.star_reward} ⭐")
    
        total_completed = UserChallenge.objects.filter(user=request.user, completed=True).count()
        if total_completed == 1:
            if award_achievement(
                request.user,
                name="First Challenge Completed",
                description="You completed your first challenge!",
                image="achievements/first_challenge.png"
            ):
                unlocked.append({
                    'name': "First Challenge Completed",
                    'description': "You completed your first challenge!",
                    'image': "achievements/first_challenge.png"
                })

        if total_completed == 3:
            if award_achievement(
                request.user,
                name="Challenge Streak",
                description="You’ve completed 3 challenges. Keep it up!",
                image="achievements/challenge_streak.png"
            ):
                unlocked.append({
                    'name': "Challenge Streak",
                    'description': "You’ve completed 3 challenges. Keep it up!",
                    'image': "achievements/challenge_streak.png"
                })
        
        if total_completed == 10:
            if award_achievement(
                request.user,
                name="Challenge Master",
                description="You’ve completed 10 challenges — you're unstoppable!",
                image="achievements/challenge_master.png"
            ):
                unlocked.append({
                    'name': "Challenge Master",
                    'description': "You’ve completed 10 challenges — you're unstoppable!",
                    'image': "achievements/challenge_master.png"
                })
        
        from datetime import datetime, timedelta

        
        def get_start_of_week():
            today = datetime.today()
            return today - timedelta(days=today.weekday())

        start_of_week = get_start_of_week()

        
        weekly_challenges = Challenge.objects.filter(
            active=True,
            created_at__gte=start_of_week
        )

        
        completed_this_week = UserChallenge.objects.filter(
            user=request.user,
            challenge__in=weekly_challenges,
            completed=True
        ).count()

        if weekly_challenges.exists() and completed_this_week == weekly_challenges.count():
            if award_achievement(
                request.user,
                name="Weekly Completionist",
                description="You've completed all challenges of the week!",
                image="achievements/weekly_completionist.png"
            ):
                unlocked.append({
                    'name': "Weekly Completionist",
                    'description': "You've completed all challenges of the week!",
                    'image': "achievements/weekly_completionist.png"
                })
        
        
        streak_days = 14
        today = datetime.today().date()
        streak_dates = [today - timedelta(days=i) for i in range(streak_days)]

        has_streak = True
        for date in streak_dates:
            completed_that_day = UserChallenge.objects.filter(
                user=request.user,
                completed=True,
                completed_at__date=date  
            ).exists()

            if not completed_that_day:
                has_streak = False
                break

        if has_streak:
            if award_achievement(
                request.user,
                name="Challenge Consistency",
                description="You completed at least one challenge every day for the past 14 days!",
                image="achievements/consistency_14.png"
            ):
                unlocked.append({
                    'name': "Challenge Consistency",
                    'description': "You completed at least one challenge every day for the past 14 days!",
                    'image': "achievements/consistency_14.png"
                })
    else:
        messages.error(request, "Вы ещё не выполнили условия этого челленджа.")

    
    if unlocked:
        request.session['just_unlocked_achievements'] = unlocked

    return redirect('challenge_detail', challenge.id)