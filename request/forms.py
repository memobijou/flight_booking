from django import forms
import phonenumbers


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

    def clean_phone(self):
        value = self.cleaned_data.get("phone")

        allowed_chars = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+", " "]
        for char in value:
            if char not in allowed_chars:
                self.add_error("phone",
                               "Sie drüfen nur Ziffern 0-9 angegeben oder eine + für die internationale Vorwahl")
                return value

        if value.startswith("+"):
            parsed_phone = phonenumbers.parse(value, None)
        else:
            parsed_phone = phonenumbers.parse(value, "DE")

        if phonenumbers.is_valid_number(parsed_phone) is False:
            self.add_error("phone", "Bitte geben Sie eine gültige Rufnummer ein")
        return value
