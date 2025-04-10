from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Appointment model.

    - Displays full name, phone number, and sent date in the admin list view.
    - Allows searching appointments by full name or phone number.
    """
    list_display = ('full_name', 'phone_number', 'sent_at')
    search_fields = ('full_name', 'phone_number')
