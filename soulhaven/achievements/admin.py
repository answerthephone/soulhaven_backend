from django.contrib import admin
from .models import Achievement, UserAchievement


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

    def has_module_permission(self, request):
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    """
    Admin configuration for the UserAchievement model.

    - Displays user, achievement, and date awarded in the admin list view.
    - Enables search by username and achievement name.
    - Orders entries by most recently awarded first.
    """
    list_display = ('user', 'achievement', 'awarded_at')
    search_fields = ('user__username', 'achievement__name')
    ordering = ('-awarded_at',)
