from django.urls import path
from . import views

urlpatterns = [
    path('<int:course_id>/progress/', views.get_course_progress, name='get_course_progress'),
    path('complete/', views.mark_course_part_complete, name='mark_course_part_complete'),
]