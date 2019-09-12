from django import forms


class CouponForm(forms.Form):
    coupon_amount = forms.IntegerField(required=True)
    stripe_token = forms.CharField(required=True)
