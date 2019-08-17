from django.urls import path
from request.views import airport_api_view, SendMailView

urlpatterns = [
    path('api/', airport_api_view),
    path('send/mail/', SendMailView.as_view(), name="mail"),
]
