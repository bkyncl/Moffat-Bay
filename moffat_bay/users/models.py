from django.db import models
from django.contrib.auth.models import User
from .states import STATES



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField(max_length=8)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(choices=STATES, max_length=50)
    zip = models.IntegerField()

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} Profile'
    
    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)