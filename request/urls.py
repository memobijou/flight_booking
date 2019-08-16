from django.urls import path
from request.views import airport_api_view

urlpatterns = [
    path('', airport_api_view),
]
