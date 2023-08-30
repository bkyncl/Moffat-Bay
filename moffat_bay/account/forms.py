from django import forms
from .models import Account
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django.contrib.auth.forms import UserCreationForm
from .states import STATE_CHOICES

class AccountForm(UserCreationForm):
    email = forms.EmailField(label="Email Address", required=True)
    phone = PhoneNumberField(widget=PhoneNumberPrefixWidget(initial='US'), label="Phone Number", required=True)
    first_name = forms.CharField(label="First Name", required=True)
    last_name = forms.CharField(label="Last Name", required=True)
    state = forms.ChoiceField(choices=STATE_CHOICES, required=False)
   

    class Meta:
        model = Account
        fields =['first_name', 'last_name', 'street', 'city', 'state', 'zip', 'phone', 'email']

class AccountUpdateForm(forms.ModelForm):
    email = forms.EmailField(label="Email Address", required=False)
    phone = PhoneNumberField(widget=PhoneNumberPrefixWidget(initial='US'), label="Phone Number", required=False)
    first_name = forms.CharField(label="First Name", required=False)
    last_name = forms.CharField(label="Last Name", required=False)
    state = forms.ChoiceField(choices=STATE_CHOICES, required=False)

    class Meta:
        model = Account
        fields =['first_name', 'last_name', 'street', 'city', 'state', 'zip', 'phone', 'email']