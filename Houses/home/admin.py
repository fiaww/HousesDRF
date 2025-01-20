from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Property, City, Rooms, PropertyImage

admin.site.register(CustomUser, UserAdmin)

admin.site.register(Property)

admin.site.register(City)

admin.site.register(Rooms)

admin.site.register(PropertyImage)
