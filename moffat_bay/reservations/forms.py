from django import forms
from django.forms.widgets import DateInput

#choice list for booking/availability search
guestChoices ={
    (1, "1 Guest"),
    (2, "2 Guests"),
    (3, "3 Guests"),
    (4, "4 Guests"),
    (5, "5 Guests"),
}

#search availability form:
class AvailabilityForm(forms.Form):
    checkInDate = forms.DateField(widget=forms.TextInput(attrs={'type':'date'}), required=True)
    checkOutDate = forms.DateField(widget=forms.TextInput(attrs={'type':'date'}), required=True)
    guests = forms.ChoiceField(choices=guestChoices, required=True)

#price change forms for admin site:
class NightlyCostPriceUpdateForm(forms.Form):
    costChange = forms.DecimalField(label="%", min_value=-100, max_value=100, decimal_places=2)

class NightlyCostPriceChangeForm(forms.Form):
    costChange = forms.DecimalField(label="$", min_value=0, max_value=1000, decimal_places=2)