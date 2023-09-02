from django import forms

class NightlyCostPriceUpdateForm(forms.Form):
    costChange = forms.DecimalField(label="%", min_value=-100, max_value=100, decimal_places=2)

class NightlyCostPriceChangeForm(forms.Form):
    costChange = forms.DecimalField(label="$", min_value=0, max_value=1000, decimal_places=2)