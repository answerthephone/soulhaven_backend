from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import CompletedGame, GameType
from stars.models import StarAction, StarHistory
from achievements.utils import award_achievement
from stars.utils import award_stars
from django.views.decorators.csrf import csrf_exempt
import json


FIRST_GAME_TYPE_ACHIEVEMENTS = {
    GameType.PUZZLES: {
        "name": "Puzzle Starter",
        "description": "You played a puzzle game for the first time!",
        "image": "achievements/puzzle_starter.png"
    },
    GameType.MANDALAS: {
        "name": "Mandala Beginner",
        "description": "You colored your first mandala!",
        "image": "achievements/mandala_beginner.png"
    },
    GameType.POP_BUBBLES: {
        "name": "Bubble Popper",
        "description": "You popped your first bubble!",
        "image": "achievements/bubble_popper.png"
    },
    GameType.FIREFLY: {
        "name": "Rhythm Rider",
        "description": "You chased your first firefly!",
        "image": "achievements/rhythm_rider.png"
    },
    GameType.PHRASES: {
        "name": "Phrase Crafter",
        "description": "You built your first phrase!",
        "image": "achievements/phrase_crafter.png"
    },
}

@csrf_exempt
@login_required
def complete_game(request):
    """
    View that handles game completion by the user.

    Trigger:
    - POST request containing 'game_type' as JSON.

    Logic:
    - Records game play.
    - Awards 50 stars.
    - Checks if it's the first time user plays this game type, and awards achievement.

    Response:
    - JSON response with status, message, and any unlocked achievements.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            game_type = data.get('game_type')

            if game_type not in GameType.values:
                return JsonResponse({'status': 'error', 'message': 'Invalid game type'}, status=400)

            CompletedGame.objects.create(user=request.user, game_type=game_type)

            award_stars(request.user, f'Game Completion: {game_type.title()}', amount=50)

            unlocked = []

            if CompletedGame.objects.filter(user=request.user, game_type=game_type).count() == 1:
                achievement_data = FIRST_GAME_TYPE_ACHIEVEMENTS.get(game_type)
                if achievement_data:
                    if award_achievement(
                        request.user,
                        name=achievement_data['name'],
                        description=achievement_data['description'],
                        image=achievement_data['image']
                    ):
                        unlocked.append({
                            'name': achievement_data['name'],
                            'description': achievement_data['description'],
                            'image': achievement_data['image']
                        })

            return JsonResponse({
                'status': 'ok',
                'message': 'Game completed. Stars awarded.',
                'achievements': unlocked
            })

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)