from django.urls import path
from .views import latest_article_api

urlpatterns = [
    path('latest/', latest_article_api, name='latest_article_api'),
]
