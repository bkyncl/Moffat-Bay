# Mark Witt / Brittany Kyncl
# CSD-440: Capstone Project
# Moffat-Bay Lodge - Bravo Team

from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

#custom user manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)



#custom user model
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=50,verbose_name="First Name", null=True, blank=True)
    last_name = models.CharField(max_length=50,verbose_name="Last Name", null=True, blank=True)
    street = models.CharField(max_length=50,verbose_name="Address", null=True, blank=True)
    city = models.CharField(max_length=50,verbose_name="City", null=True, blank=True)
    state = models.CharField(max_length=50,verbose_name="State", null=True, blank=True)
    zip = models.CharField(max_length=8,verbose_name="Zipcode", null=True, blank=True)
    phone = PhoneNumberField(verbose_name="Phone Number", blank=True, null=True)

    class Meta:
        verbose_name_plural = "User Accounts"

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
#mailing list model
class MailingList(models.Model):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)

    class Meta:
        verbose_name_plural = "Mailing List"

    def __str__(self) -> str:
        return self.email
    
    def __str__(name) -> str:
        return name.email
