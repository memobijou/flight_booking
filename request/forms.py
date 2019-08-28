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

    def clean_adults(self):
        value = self.cleaned_data.get("adults")
        print(f"sadiqi: {value}")
        if value == 0:
            self.add_error("adults", "Sie müssen mindestens einen Erwachsen auswählen")
        if value < 0:
            self.add_error("adults", "Sie können nur Zahlen größer als 0 eingeben")
        return value

    def clean_children(self):
        value = self.cleaned_data.get("children")
        if value < 0:
            self.add_error("children", "Sie können nur Zahlen größer als 0 eingeben")
        return value
