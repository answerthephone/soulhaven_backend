from django.db import models
from django.contrib.auth.models import User

class ChallengeType(models.TextChoices):
    """
    Enum-like class for defining types of challenges.

    Options:
    - FINISH_COURSES: User must complete a certain number of courses.
    - FINISH_GAMES: User must complete a certain number of game types.
    - CUSTOM: Manually triggered challenges not tied to specific progress.
    """
    FINISH_COURSES = 'finish_courses', 'Finish N Courses'
    FINISH_GAMES = 'finish_games', 'Finish N Games'
    CUSTOM = 'custom', 'Manual Trigger'

class Challenge(models.Model):
    """
    Represents a challenge that users can complete for rewards.

    Fields:
    - name: The title of the challenge (e.g., "Complete 3 Courses").
    - description: A detailed explanation of what the challenge requires.
    - type: Type of challenge from ChallengeType (e.g., FINISH_COURSES).
    - target_value: The goal amount (e.g., complete 3 courses/games).
    - course_title: (Optional) Specific course or game title to match (used for single-item challenges).
    - star_reward: Number of stars awarded upon completion.
    - active: Whether the challenge is currently available.
    - created_at: Timestamp of when the challenge was created.

    Methods:
    - __str__(): Returns the challenge's name for easy identification.
    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(max_length=50, choices=ChallengeType.choices)
    target_value = models.PositiveIntegerField()
    course_title = models.CharField(max_length=255, blank=True, null=True)
    star_reward = models.PositiveIntegerField()
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class UserChallenge(models.Model):
    """
    Represents the progress of a specific user on a specific challenge.

    Fields:
    - user: The user who is attempting the challenge.
    - challenge: The challenge being tracked.
    - progress: Current progress value (e.g., 2 out of 3).
    - completed: Boolean indicating whether the challenge is completed.
    - completed_at: Timestamp when the challenge was completed.

    Meta:
    - unique_together: Ensures that each user can only have one record per challenge.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    progress = models.PositiveIntegerField(default=0)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'challenge')
