# Mark Witt / Brittany Kyncl
# CSD-440: Capstone Project
# Moffat-Bay Lodge - Bravo Team

from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    verbose_name ="Account Manager"