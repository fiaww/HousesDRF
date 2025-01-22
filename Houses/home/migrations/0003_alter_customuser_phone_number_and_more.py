# Generated by Django 5.1.5 on 2025-01-21 07:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_property_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(blank=True, max_length=10, unique=True, validators=[django.core.validators.RegexValidator(message='Введите ваш номер телефона после +7', regex='^\\+?1?\\d{10}$')]),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(max_length=100),
        ),
    ]
