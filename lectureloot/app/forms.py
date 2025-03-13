from django import forms
from .models import Listing

# Listing form
class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing 
        fields = ['title', 'category', 'description', 'image', 'end_datetime']