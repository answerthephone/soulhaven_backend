from django.db import models
from django.contrib.auth.models import User


class Achievement(models.Model):
    """
    Represents a single achievement that users can unlock.

    Fields:
    - name: The unique name of the achievement (e.g. "First Course Completed").
    - description: A short explanation of what the achievement is for.
    - image: Optional image (e.g. icon or badge) associated with the achievement.

    Methods:
    - __str__(): Returns the name of the achievement.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='achievements/', blank=True, null=True)

    def __str__(self):
        return self.name


class UserAchievement(models.Model):
    """
    Represents the relationship between a user and an unlocked achievement.

    Fields:
    - user: The user who unlocked the achievement.
    - achievement: The achievement that was awarded.
    - awarded_at: Timestamp when the achievement was granted.

    Meta:
    - unique_together: Ensures each achievement can be awarded only once per user.

    Methods:
    - __str__(): Returns a readable string like "username - achievement name".
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    awarded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'achievement') 

    def __str__(self):
        return f"{self.user.username} - {self.achievement.name}"
