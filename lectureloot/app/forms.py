from django import forms
from .models import Listing, Media

# Listing form
class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing 
        fields = ['title', 'category', 'description']

# Media form under listing form
class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ['file'] # media_type will be deduced automatically

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file'].widget.attrs.update({'accept': 'image/*,video/*'})

#maximum of 10 media per listing
MediaFormSet = forms.modelformset_factory(Media, form=MediaForm, extra=1, max_num=10)
