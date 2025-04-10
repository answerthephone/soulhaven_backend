from django.urls import path
from . import views

urlpatterns = [
    path('<int:expert_id>/', views.expert_detail, name='expert_detail'),
]