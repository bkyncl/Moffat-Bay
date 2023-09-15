# Mark Witt / Brittany Kyncl
# CSD-440: Capstone Project
# Moffat-Bay Lodge - Bravo Team

from django import forms
from django.forms.widgets import NumberInput
from .guests import guestChoices
from rooms.models import RoomChoices, Rooms
from django.core.validators import RegexValidator
#choice list for booking/availability search


#search availability form and booking form:
class AvailabilityForm(forms.Form):
    checkInDate = forms.DateField(widget=forms.NumberInput(attrs={'type':'date'}), required=True)
    checkOutDate = forms.DateField(widget=forms.NumberInput(attrs={'type':'date'}), required=True)
    guests = forms.ChoiceField(choices=guestChoices, required=True)

#price change forms for admin site:
class NightlyCostPriceUpdateForm(forms.Form):
    costChange = forms.DecimalField(label="%", min_value=-100, max_value=100, decimal_places=2)

class NightlyCostPriceChangeForm(forms.Form):
    costChange = forms.DecimalField(label="$", min_value=0, max_value=1000, decimal_places=2)

class MyReservationSearchForm(forms.Form):
    searchConfirm = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Ex: 4FA0J89'}),
        label='',  # Set the label to an empty string
        validators=[
            RegexValidator(
                regex=r'^[0-9a-zA-Z]{7}$',
                message="Please enter a 7 character confirmation number.",
                code='invalid_confirmation_number'
            )
        ],
        error_messages={
            'required': 'This field is required. Please enter your confirmation number.'
        }
    )
