from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from PIL import Image

#custom user account manager - integrates django's user backend with our custom user account model
#this integrates both so we can use out custom model, and use email to login instead of usernames
class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an email address.")
        if not username:
            raise ValueError("Users must have a username.")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.is_admin=True
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user


#our custom user account model, storing all user account data in one table. 
#includes the required fields for the Django user model, so all features will work correctly
class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    first_name = models.CharField(max_length=50,verbose_name="First Name", null=True, blank=True)
    last_name = models.CharField(max_length=50,verbose_name="Last Name", null=True, blank=True)
    street = models.CharField(max_length=50,verbose_name="Address", null=True, blank=True)
    city = models.CharField(max_length=50,verbose_name="City", null=True, blank=True)
    state = models.CharField(max_length=50,verbose_name="State", null=True, blank=True)
    zip = models.CharField(max_length=8,verbose_name="Zipcode", null=True, blank=True)
    phone = PhoneNumberField(verbose_name="Phone Number", blank=True, null=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    hide_email = models.BooleanField(default=True)
    image = models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics')

    

    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
    
    #custom save method: will resize any profile pic user chooses to a managable thumbnail size before saving the image to the server.
    def save(self, *args, **kwargs):
        super(Account, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

