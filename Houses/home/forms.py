from django import forms
from .models import Property


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['title', 'description', 'price', 'city', 'rooms', 'property_type', 'location', 'is_for_sale', 'is_for_rent']
