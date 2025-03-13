from django import forms
from .models import Listing, CustomUser
from django.contrib.auth import get_user_model

# Listing form
class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing 
        fields = ['title', 'price', 'category', 'description', 'image']

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'first_name', 'last_name', 'password' ]

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('rating', 'profile_project',)