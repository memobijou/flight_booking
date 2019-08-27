from django import forms


class RequestForm(forms.Form):
    flight_from = forms.CharField(required=True)
    flight_to = forms.CharField(required=True)
    departure_date = forms.DateField(required=True)
    return_flight_date = forms.DateField(required=True)
    adults = forms.IntegerField(required=True)
    children = forms.IntegerField()
    travel_class = forms.CharField(required=True)
    flight_type = forms.CharField(required=True)
    phone = forms.CharField(required=True)
