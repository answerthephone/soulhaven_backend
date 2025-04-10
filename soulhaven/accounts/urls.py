from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.user_register, name='user_register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),

    path('account/', views.personal_account_view, name='personal_account'),
    path('profile/', views.profile_view, name='profile'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('star-history/', views.star_history_view, name='star_history'),
    path('achievements/', views.user_achievements, name='achievements'),
]