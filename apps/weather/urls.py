from django.urls import path
from .views import weather_page


urlpatterns = [
    path("", weather_page, name="weather"),
]
