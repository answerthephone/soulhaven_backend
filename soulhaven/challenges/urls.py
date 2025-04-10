from django.urls import path
from . import views

urlpatterns = [
    path('<int:challenge_id>/', views.challenge_detail, name='challenge_detail'),
    path('<int:challenge_id>/complete/', views.complete_challenge, name='complete_challenge'),
]