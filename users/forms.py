from typing import Any
from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.forms import UserChangeForm, UserCreationForm


class PersonalizedUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ('username', 'email',)


class UserUpdateForm(UserChangeForm):

    class Meta:
        model = User
        fields = ['username', 'email']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'password' in self.fields:
            del self.fields['password']


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['profile_photo']

    def clean_profile_photo(self):
        image = self.cleaned_data.get('profile_photo')

        if image:
            allowed_formats = ['jpg', 'jpeg', 'png', 'webp']
            extension = image.name.split('.')[-1].lower()
            if extension not in allowed_formats:
                self.add_error('profile_photo', f"Formato {extension} não é permitido. Tente um desses formatos: {', '.join(allowed_formats)} ")
        return image
