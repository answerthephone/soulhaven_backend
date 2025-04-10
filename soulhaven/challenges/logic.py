from django.utils import timezone
from challenges.models import Challenge, UserChallenge, ChallengeType
from stars.models import StarAction, StarHistory
from courses.models import CourseProgress
from django.utils import timezone
from games.models import CompletedGame
from stars.utils import award_stars

def give_stars(user, challenge):
    """
    Awards stars for a completed challenge if the user hasn't already been rewarded.

    Parameters:
    - user: The User instance to award stars to.
    - challenge: The Challenge instance that has been completed.

    Notes:
    - Uses a StarHistory check to prevent duplicate star rewards.
    """
    if not StarHistory.objects.filter(user=user, action__name=f"Challenge Completion: {challenge.name}").exists():
        award_stars(user, f"Challenge Completion: {challenge.name}", amount=challenge.star_reward)

def check_course_challenges(user, completed_course):
    """
    Checks and updates the progress of active course-related challenges for a user.

    Parameters:
    - user: The User instance to evaluate.
    - completed_course: The Course instance that was just completed.

    Logic:
    - If the challenge has a specific course title and target of 1, match it directly.
    - Otherwise, compare total completed test parts (distinct courses) to the challenge's target.
    - Updates progress and awards stars upon challenge completion.
    """
    challenges = Challenge.objects.filter(type=ChallengeType.FINISH_COURSES, active=True)
    for challenge in challenges:
        uc, _ = UserChallenge.objects.get_or_create(user=user, challenge=challenge)
        if uc.completed:
            continue

        if challenge.target_value == 1 and challenge.course_title:
            if completed_course.title == challenge.course_title:
                uc.completed = True
                uc.completed_at = timezone.now()
                uc.progress = 1
                uc.save()
                give_stars(user, challenge)
        else:
            completed_count = CourseProgress.objects.filter(user=user, part='test').values('course').distinct().count()
            if completed_count >= challenge.target_value:
                uc.completed = True
                uc.completed_at = timezone.now()
                uc.progress = challenge.target_value
                uc.save()
                give_stars(user, challenge)
            else:
                uc.progress = completed_count
                uc.save()

def check_game_challenges(user, completed_game_type: str):
    """
    Checks and updates the progress of active game-related challenges for a user.

    Parameters:
    - user: The User instance to evaluate.
    - completed_game_type: A string representing the game that was just completed.

    Logic:
    - If the challenge targets a specific game and target_value is 1, match directly.
    - Otherwise, count how many unique game types the user has completed.
    - Updates progress and awards stars upon challenge completion.
    """
    challenges = Challenge.objects.filter(type=ChallengeType.FINISH_GAMES, active=True)

    for challenge in challenges:
        uc, _ = UserChallenge.objects.get_or_create(user=user, challenge=challenge)
        if uc.completed:
            continue

        if challenge.target_value == 1 and challenge.course_title:
            if completed_game_type == challenge.course_title:
                uc.completed = True
                uc.completed_at = timezone.now()
                uc.progress = 1
                uc.save()
                give_stars(user, challenge)
        else:
            game_count = CompletedGame.objects.filter(
                user=user
            ).values('game_type').distinct().count()

            if game_count >= challenge.target_value:
                uc.completed = True
                uc.completed_at = timezone.now()
                uc.progress = game_count
                uc.save()
                give_stars(user, challenge)
            else:
                uc.progress = game_count
                uc.save()