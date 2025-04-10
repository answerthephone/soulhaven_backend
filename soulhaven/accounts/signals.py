from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from .models import UserProfile
from stars.models import StarAction, StarHistory
from datetime import date
from stars.utils import award_stars


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal: Creates a UserProfile when a new User is created.

    - Automatically sets the nickname to match the username.
    - Awards a star reward for registration.
    """
    if created:
        
        UserProfile.objects.create(user=instance, nickname=instance.username)

        award_stars(instance, action_name='Registration Reward', amount=10)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal: Ensures the UserProfile is saved when the User is saved.

    - Keeps the user profile in sync after updates.
    """
    instance.userprofile.save()


@receiver(user_logged_in)
def reward_login_if_first_today(sender, request, user, **kwargs):
    """
    Signal: Rewards user with stars if logging in for the first time today.

    - Tracks login dates in log_ins list.
    - Awards daily login stars only once per day.
    """
    profile = user.userprofile
    today = date.today()


    if profile.log_ins is None:
        profile.log_ins = []

    if today not in profile.log_ins:
        profile.log_ins.append(today)
        profile.save()

        award_stars(user=request.user, action_name='Daily Login Reward', amount=50)
