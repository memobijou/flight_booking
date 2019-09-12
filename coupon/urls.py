from django.urls import path
from coupon.views import coupon_view, coupon_payment_view

urlpatterns = [
    path('booking/', coupon_view, name="coupon"),
    path('payment/', coupon_payment_view, name="payment")
]
