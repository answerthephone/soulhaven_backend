from django.contrib import admin
from .models import StarAction


@admin.register(StarAction)
class StarActionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'amount')
    search_fields = ('name',)
    ordering = ('id',)

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