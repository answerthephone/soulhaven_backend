from django.urls import path
from .views import homepage_data_api

urlpatterns = [
    path('api/homepage/', homepage_data_api, name='homepage_data_api'),
]