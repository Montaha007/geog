from django import forms
from .models import GeoHistory

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'point', 'polygon']  # No 'user'
        widgets={
            'points': forms.HiddenInput(),
            'polygon': forms.HiddenInput(),
        }