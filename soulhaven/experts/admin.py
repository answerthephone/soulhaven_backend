from django.contrib import admin
from .models import Expert

@admin.register(Expert)
class ExpertAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization', 'email', 'experience')
    search_fields = ('name', 'specialization', 'email')
