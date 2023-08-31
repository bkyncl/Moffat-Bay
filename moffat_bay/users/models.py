from django.db import models
from django.contrib.auth.models import User
from .states import STATES
from PIL import Image



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(choices=STATES, max_length=50)
    zip = models.CharField(max_length=6)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} Profile'
    
def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)