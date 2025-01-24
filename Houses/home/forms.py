from django import forms
from .models import Property, PropertyImage


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['title', 'description', 'price', 'city', 'rooms', 'property_type', 'location', 'is_for_sale', 'is_for_rent']


class PropertyImageForm(forms.ModelForm):
    class Meta:
        model = PropertyImage
        fields = ['image']


class PropertyFilterForm(forms.Form):
    PROPERTY_TYPES = [
        ('', 'Все типы'),
        ('house', 'Дом'),
        ('apartment', 'Квартира'),
    ]

    ROOMS = [
        ('', 'Любое количество'),
        ('1', 'Студия'),
        ('2', '1'),
        ('3', '2'),
        ('4', '3'),
        ('5', '4'),
        ('6', '5'),
        ('7', '6'),
    ]

    CITY = [
        ('', 'Все города'),
        ('1', 'Москва'),
        ('2', 'Санкт-Петербург'),
        ('3', 'Казань'),
        ('4', 'Нижний Новгород'),
        ('5', 'Екатеринбург'),
    ]

    RENT_OR_SALE = [
        ('', 'Все варианты'),
        ('is_for_rent', 'Аренда'),
        ('is_for_sale', 'Покупка'),
    ]

    property_type = forms.ChoiceField(choices=PROPERTY_TYPES, required=False)
    min_price = forms.DecimalField(required=False, min_value=0)
    max_price = forms.DecimalField(required=False, min_value=0)
    rooms = forms.ChoiceField(choices=ROOMS, required=False)
    city = forms.ChoiceField(choices=CITY, required=False)
    rent_or_sale = forms.ChoiceField(choices=RENT_OR_SALE, required=False)
