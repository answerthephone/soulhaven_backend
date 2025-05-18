from django.urls import path
from . import views

urlpatterns = [
    path('<int:challenge_id>/', views.challenge_detail_api, name='challenge_detail_api'),
    path('<int:challenge_id>/complete/', views.complete_challenge_api, name='complete_challenge_api'),
]