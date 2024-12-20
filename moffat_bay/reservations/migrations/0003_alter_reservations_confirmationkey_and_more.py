# Generated by Django 4.2.4 on 2023-09-04 16:02
# Mark Witt / Brittany Kyncl
# CSD-440: Capstone Project
# Moffat-Bay Lodge - Bravo Team

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0002_reservations'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservations',
            name='confirmationKey',
            field=models.CharField(max_length=7),
        ),
        migrations.AlterField(
            model_name='reservations',
            name='totalPrice',
            field=models.DecimalField(decimal_places=2, max_digits=11),
        ),
    ]
