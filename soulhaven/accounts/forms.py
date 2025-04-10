from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class UserEditForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['email']

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nickname', 'avatar']
