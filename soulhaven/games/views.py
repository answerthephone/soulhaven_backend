from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import CompletedGame, GameType
from stars.models import StarAction, StarHistory
from achievements.utils import award_achievement
from stars.utils import award_stars


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

@login_required
def complete_game(request):
    """
    View that handles game completion by the user.

    Trigger:
    - POST request containing 'game_type'.

    Logic:
    - Creates a CompletedGame record for the user and specified game type.
    - Awards 50 stars for the completion.
    - Checks if this is the user's first time completing this game type:
        - If yes, awards an achievement defined in FIRST_GAME_TYPE_ACHIEVEMENTS.

    Response:
    - On success:
        - status: "ok"
        - message: Confirmation message
        - achievements: List of newly unlocked achievements (if any)
    - On failure:
        - status: "error"
        - HTTP 400 with error message
    """
    if request.method == 'POST':
        game_type = request.POST.get('game_type')

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

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
