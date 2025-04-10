from django.db import models
from django.contrib.auth.models import User

class GameType(models.TextChoices):
    """
    Enum-like class representing the types of mini-games available on the platform.

    Options:
    - PUZZLES: Logic-based or visual puzzle games.
    - MANDALAS: Coloring mandala-based activities.
    - POP_BUBBLES: Tap-and-pop reaction-based game.
    - FIREFLY: Rhythm-following game with moving fireflies.
    - PHRASES: Game for constructing meaningful phrases from given words.
    """
    PUZZLES = 'puzzles', 'Puzzles'
    MANDALAS = 'mandalas', 'Mandalas'
    POP_BUBBLES = 'pop_bubbles', 'Pop the Bubble'
    FIREFLY = 'firefly', 'Firefly Rhythm'
    PHRASES = 'phrases', 'Phrase Builder'

class CompletedGame(models.Model):
    """
    Tracks when a user plays a specific mini-game.

    Fields:
    - user: The user who played the game.
    - game_type: The type of game played (from GameType).
    - played_at: Timestamp when the game was completed.

    Methods:
    - __str__(): Returns a readable string like 'username - Game Type - DateTime'.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game_type = models.CharField(max_length=50, choices=GameType.choices)
    played_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_game_type_display()} - {self.played_at.strftime('%Y-%m-%d %H:%M')}"
