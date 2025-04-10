from django import forms
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['full_name', 'phone_number']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Укажите свое ФИО'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Укажите номер телефона'}),
        }