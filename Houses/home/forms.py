from django import forms
from django.core.exceptions import ValidationError

from .models import Property, PropertyImage


class PropertyForm(forms.ModelForm):
    LISTING_TYPE_CHOICES = [
        ('sale', 'Продажа'),
        ('rent', 'Аренда'),
    ]

    listing_type = forms.ChoiceField(
        choices=LISTING_TYPE_CHOICES,
        widget=forms.RadioSelect,
        label="Тип объявления",
    )

    class Meta:
        model = Property
        fields = ['title', 'description', 'price', 'city', 'rooms', 'property_type', 'location']

    def save(self, commit=True):
        property = super().save(commit=False)
        listing_type = self.cleaned_data.get('listing_type')
        if listing_type == 'sale':
            property.is_for_sale = True
            property.is_for_rent = False
        if listing_type == 'rent':
            property.is_for_sale = False
            property.is_for_rent = True
        if commit:
            property.save()
        return property


class PropertyImageForm(forms.ModelForm):
    class Meta:
        model = PropertyImage
        fields = ['image']

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image:
            raise ValidationError("Изображение обязательно для загрузки.")
        return image


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
