from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


#create profile upon creation of user account
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwags):
    if created:
        Profile.objects.create(user=instance)


#save profile upon update of user account
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()