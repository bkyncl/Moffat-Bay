from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.modelfields import PhoneNumberField
from .models import Profile
from .states import STATES

class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(label="First Name", required=True)
    last_name = forms.CharField(label="Last Name", required=True)
    dob = forms.DateField(label="Date of Birth", required=True)
    street = forms.CharField(label="Street Address")
    city = forms.CharField(label="City", max_length=100)
    state = forms.CharField(label="State", choices=STATES)
    zip = forms.IntegerField(label="Zip Code", max_value=99999)
    email = forms.EmailField(label="E-Mail", required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'dob', 'street', 'city', 'state', 'zip', 'email', 'password1', 'password2']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profilefields = ['dob', 'street', 'city', 'state', 'zip', 'email']