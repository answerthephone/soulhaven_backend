from django.urls import path
from .views import complete_game

urlpatterns = [
    path('complete/', complete_game, name='complete_game'),
]
