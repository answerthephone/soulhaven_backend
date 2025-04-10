from django.urls import path
from . import views

urlpatterns = [
    path('latest-article/', views.latest_article_detail, name='latest_article'),
]
