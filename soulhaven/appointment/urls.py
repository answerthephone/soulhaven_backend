from django.urls import path
from .views import create_appointment_api

urlpatterns = [
    path('create/', create_appointment_api, name='create_appointment_api'),
]