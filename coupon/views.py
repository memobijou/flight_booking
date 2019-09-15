from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
import stripe
from stripe import error
import random
from coupon.forms import CouponForm


# Create your views here.
def coupon_view(request):
    context = {"STRIPE_PUBLISHABLE": settings.STRIPE_PUBLISHABLE, "months_dropdown": range(1, 13),
               "years_dropdown": range(2019, 2051)}
    return render(request, "flightairline/coupon/coupon.html", context)


def coupon_payment_view(request):
    if request.POST:
        form = CouponForm(request.POST)
        if form.is_valid() is True:
            token = form.cleaned_data.get("stripe_token")
            coupon_amount = form.cleaned_data.get("coupon_amount")

            try:
                coupon = generate_coupon_code(8)
                stripe.Charge.create(api_key=settings.STRIPE_SECRET, amount=int(coupon_amount)*int(100), currency="EUR",
                                     description=f"{coupon}", card=token)
            except error.CardError as e:
                print(e)
                return JsonResponse(data={"message": "Ihre Karte wurde abgelehnt"}, status=400, safe=False)
            return JsonResponse(data={"message": "Zahlung erfolgreich", "coupon": f"{coupon}"}, status=201, safe=False)
        else:
            return JsonResponse(data={"message": "form_error", "errors": form.errors}, status=400, safe=False)


def generate_coupon_code(num_chars):
    code_chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    code = ''
    for i in range(0, num_chars):
        slice_start = random.randint(0, len(code_chars) - 1)
        code += code_chars[slice_start: slice_start + 1]
    return code
