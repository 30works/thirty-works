from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile
from blog.models import Post


class MyUserCreationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User # ensure data is saved to User model
        fields = ['username',
                  'email',
                  'password1',
                  'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User # ensure data is saved to User model
        fields = ['username',
                  'email']

class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profilepic', 'insta_handler', 'url']