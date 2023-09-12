# Mark Witt / Brittany Kyncl
# CSD-440: Capstone Project
# Moffat-Bay Lodge - Bravo Team

from django import forms
from .models import CustomUser, MailingList
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import EmailValidator
from .states import STATE_CHOICES

class AccountForm(UserCreationForm):
    email = forms.EmailField(label="Email Address", required=True)
    phone = PhoneNumberField(widget=PhoneNumberPrefixWidget(initial='US'), label="Phone Number", required=True)
    first_name = forms.CharField(label="First Name", required=True)
    last_name = forms.CharField(label="Last Name", required=True)
    state = forms.ChoiceField(choices=STATE_CHOICES, required=False)
   

    class Meta:
        model = CustomUser
        fields =['first_name', 'last_name', 'street', 'city', 'state', 'zip', 'phone', 'email']

class AccountUpdateForm(forms.ModelForm):
    email = forms.EmailField(label="Email Address", required=False)
    phone = PhoneNumberField(widget=PhoneNumberPrefixWidget(initial='US'), label="Phone Number", required=False)
    first_name = forms.CharField(label="First Name", required=False)
    last_name = forms.CharField(label="Last Name", required=False)
    state = forms.ChoiceField(choices=STATE_CHOICES, required=False)

    class Meta:
        model = CustomUser
        fields =['first_name', 'last_name', 'street', 'city', 'state', 'zip', 'phone', 'email']

class MailListForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'Enter your email'}))

    class Meta:
        model = MailingList
        fields = ['email',]

#form class for email contact form on 'contact_us.html'
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label="Your Name")
    email = forms.EmailField(label="Your Email", validators=[EmailValidator(message="Please enter a valid email address.")])
    message = forms.CharField(widget=forms.Textarea, label="Your Message")