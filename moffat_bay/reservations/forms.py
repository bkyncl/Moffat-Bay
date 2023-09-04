from django import forms
from django.forms.widgets import DateInput
from .utilities import guestChoices

#search availability form:
class AvailabilityForm(forms.Form):
    checkInDate = forms.DateField(widget=DateInput, required=True)
    checkOutDate = forms.DateField(widget=DateInput, required=True)
    guests = forms.ChoiceField(choices=guestChoices, required=True)

#price change forms for admin site:
class NightlyCostPriceUpdateForm(forms.Form):
    costChange = forms.DecimalField(label="%", min_value=-100, max_value=100, decimal_places=2)

class NightlyCostPriceChangeForm(forms.Form):
    costChange = forms.DecimalField(label="$", min_value=0, max_value=1000, decimal_places=2)