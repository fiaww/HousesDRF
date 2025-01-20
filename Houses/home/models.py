from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{10}$',
                                 message="Введите ваш номер телефона после +7")
    phone_number = models.CharField(validators=[phone_regex], max_length=10, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.username


class Rooms(models.Model):
    number = models.CharField(max_length=50, db_index=True)

    class Meta:
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'

    def __str__(self):
        return self.number


class City(models.Model):
    city_name = models.CharField(max_length=50, db_index=True)

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.city_name


class Property(models.Model):
    PROPERTY_TYPES = [
        ('house', 'House'),
        ('apartment', 'Apartment'),
    ]

    title = models.CharField(max_length=60)
    description = models.TextField(blank=True)
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    rooms = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    is_for_sale = models.BooleanField(default=False)
    is_for_rent = models.BooleanField(default=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='properties')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    # image = models.ImageField(upload_to='property_images/')

    def __str__(self):
        return self.title


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='property_images/')

    def __str__(self):
        return f"Image for {self.property}"
