from .models import Achievement, UserAchievement

def award_achievement(user, name, description=None, image=None):
    """
    Awards an achievement to a user if they haven't received it yet.

    Parameters:
    - user: The User instance receiving the achievement.
    - name: Unique name of the achievement.
    - description (optional): Description of the achievement (used if created).
    - image (optional): Image path or object associated with the achievement (used if created).

    Returns:
    - True if the achievement was awarded.
    - False if the user already had this achievement.
    """
    achievement, _ = Achievement.objects.get_or_create(
        name=name,
        defaults={
            'description': description or '',
            'image': image  
        }
    )

    if not UserAchievement.objects.filter(user=user, achievement=achievement).exists():
        UserAchievement.objects.create(user=user, achievement=achievement)
        return True 
    return False