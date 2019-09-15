"""flight_booking URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from flight_booking.views import phonenumber_validation_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name="flightairline/index.html"), name="main"),
    path('vacation/', TemplateView.as_view(template_name="flightairline/vacation/vacation.html"), name="vacation"),
    path('flughafen/', TemplateView.as_view(template_name="flightairline/airport/airport.html"), name="airport"),
    path('flight-route/', TemplateView.as_view(template_name="flightairline/flight_route/flight_route.html"),
         name="flight_route"),
    path('tour-operator/', TemplateView.as_view(template_name="flightairline/tour_operator/tour_operator.html"),
         name="tour_operator"),
    path('last-minute/', TemplateView.as_view(template_name="flightairline/last_minute/last_minute.html"),
         name="last_minute"),
    path('cheap-flight/', TemplateView.as_view(template_name="flightairline/cheap_flight/cheap_flight.html"),
         name="cheap_flight"),
    path('airline/', TemplateView.as_view(template_name="flightairline/airline/airline.html"),
         name="airline"),
    path('flight/', TemplateView.as_view(template_name="flightairline/flight/flight.html"),
         name="flight"),
    path('coupon/', include(('coupon.urls', "coupon"), namespace="coupon")),
    path('airport/', include(('request.urls', "request"), namespace="request")),
    path('phone/validation', phonenumber_validation_view, name="validate_phone"),
]
