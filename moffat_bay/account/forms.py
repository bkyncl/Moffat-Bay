from django import forms
from .models import Account
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django.contrib.auth.forms import UserCreationForm

class AccountForm(UserCreationForm):
    
    email = forms.EmailField(label="Email Address")
    phone = PhoneNumberField(widget=PhoneNumberPrefixWidget(initial='US'), label="Phone Number", required=False)
    first_name = forms.CharField(label="First Name", required=True)
    last_name = forms.CharField(label="Last Name", required=True)
   

    class Meta:
        model = Account
        fields =['first_name', 'last_name', 'street', 'city', 'state', 'zip', 'phone', 'email']