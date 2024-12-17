from django.urls import path
from app_datetime.views import datetime_view

urlpatterns = [
    path('datetime/', datetime_view)
]
