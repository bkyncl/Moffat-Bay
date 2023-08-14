from django import forms
from django.forms.widgets import NumberInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from .states import STATES

class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(label="First Name", required=True)
    last_name = forms.CharField(label="Last Name", required=True)
    street = forms.CharField(label="Street Address")
    city = forms.CharField(label="City", max_length=100)
    state = forms.ChoiceField(choices=STATES, label="State")
    zip = forms.CharField(label="Zip Code", max_length=6)
    email = forms.EmailField(label="E-Mail", required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'street', 'city', 'state', 'zip', 'email', 'username', 'password1', 'password2']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [ 'street', 'city', 'state', 'zip', 'image']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['email']