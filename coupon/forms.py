from django import forms


coupon_amounts = [100, 150, 200, 250, 300, 350, 400, 450, 500]


class CouponForm(forms.Form):
    coupon_amount = forms.IntegerField(required=True)
    stripe_token = forms.CharField(required=True)

    def clean_coupon_amount(self):
        data = self.cleaned_data.get("coupon_amount")
        if data > 500:
            self.add_error("coupon_amount", "Der Betrag darf nicht höher als 500€ sein")
        return data
