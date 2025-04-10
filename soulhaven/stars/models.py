from django.db import models
from django.contrib.auth.models import User


class StarAction(models.Model):
    """
    Represents a unique action that grants stars to users.

    Fields:
    - id: Auto-generated primary key.
    - name: Unique name of the action (e.g. "Daily Login Reward", "Course Completion").
    - amount: Number of stars awarded for performing this action.

    Methods:
    - __str__(): Returns a readable string including the name and star amount (e.g. "Course Completion (+200 ⭐)").
    """
    id = models.AutoField(primary_key=True)  # Automatically generated
    name = models.CharField(max_length=100, unique=True)
    amount = models.IntegerField()

    def __str__(self):
        return f"{self.name} (+{self.amount} ⭐)"


class StarHistory(models.Model):
    """
    Records when a user earns stars and for which action.

    Fields:
    - user: The user who earned the stars.
    - action: The StarAction that granted the stars (nullable on delete).
    - earned_at: Timestamp of when the stars were awarded.

    Methods:
    - __str__(): Displays a summary like "username - Action Name (+Amount)".
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.ForeignKey(StarAction, on_delete=models.SET_NULL, null=True)
    earned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.action.name} (+{self.action.amount})"