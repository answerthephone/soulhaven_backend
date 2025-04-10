from django.contrib.auth.models import User
from django.db import models
from django.contrib.postgres.fields import ArrayField
from datetime import date


class UserProfile(models.Model):
    """
    Extends the built-in User model with additional profile-related data.

    Fields:
    - user: One-to-one link to Django's User model.
    - nickname: Optional public display name (can differ from username).
    - age: The user's age (default is 0).
    - level: The user's current level (based on stars earned).
    - stars: Total stars accumulated by the user through platform activities.
    - avatar: Optional profile picture uploaded by the user.
    - log_ins: Array of datetime entries representing days the user logged in,
               used for tracking daily activity and streaks.

    Methods:
    - __str__(): Returns a human-readable string representation of the profile.
    - has_logged_in_today(): Returns True if the user has logged in today.
    - add_login_date(): Adds today to log_ins if not already present and returns
                        True if added, False otherwise.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=150, blank=True)
    age = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    stars = models.IntegerField(default=0)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    log_ins = ArrayField(models.DateTimeField(), blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile"
    
    def has_logged_in_today(self):
        """
        Checks whether the user has already logged in today.

        Returns:
            bool: True if today's date is in log_ins, else False.
        """
        return date.today() in (self.log_ins or [])

    def add_login_date(self):
        """
        Adds today's date to log_ins if it's not already there.

        Returns:
            bool: True if today's date was added, False if it was already present.
        """
        today = date.today()
        self.log_ins = list(set(self.log_ins or []))
        if today not in self.log_ins:
            self.log_ins.append(today)
            return True
        return False
