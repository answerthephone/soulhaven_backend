from django.urls import path
from .views import expert_detail_api

urlpatterns = [
    path('<int:expert_id>/', expert_detail_api, name='expert_detail_api'),
]
