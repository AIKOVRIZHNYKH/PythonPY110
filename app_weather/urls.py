from django.urls import path
from app_weather.views import my_weather_view

urlpatterns = [
    path('weather/', my_weather_view)
]





