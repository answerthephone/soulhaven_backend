from .models import StarAction, StarHistory
from accounts.models import UserProfile

def award_stars(user, action_name, amount=None):
    """
    Centralized function to award stars to a user for a specific action.

    Parameters:
    - user (User): The user receiving the stars.
    - action_name (str): A unique name describing the action (e.g., "Daily Login Reward").
    - amount (int, optional): Override for star amount to award. 
                              If None and the action exists, uses the stored amount.

    Logic:
    - Retrieves or creates a StarAction by name.
    - If the action already exists and amount differs, updates the stored amount.
    - Creates a StarHistory entry for the user and the action.
    - Increases the user's star count and updates their level (1 level per 1000 stars).

    Returns:
    - dict: {
        'name': str — name of the action,
        'amount': int — stars awarded,
        'awarded': True,
        'level': int — new user level,
        'stars': int — total stars after award
      }
    """
    action, created = StarAction.objects.get_or_create(
        name=action_name,
        defaults={'amount': amount or 0}
    )

    if amount is not None and not created and amount != action.amount:
        action.amount = amount
        action.save()

    StarHistory.objects.create(user=user, action=action)

    profile = user.userprofile
    profile.stars += action.amount

    new_level = (profile.stars // 1000) + 1
    if new_level > profile.level:
        profile.level = new_level

    profile.save()

    return {
        'name': action.name,
        'amount': action.amount,
        'awarded': True,
        'level': profile.level,
        'stars': profile.stars,
    }
