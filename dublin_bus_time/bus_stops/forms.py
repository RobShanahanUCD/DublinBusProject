from django import forms


class JourneyForm(forms.Form):
    route = forms.CharField(max_length=6)
    time = forms.CharField(max_length=15)

