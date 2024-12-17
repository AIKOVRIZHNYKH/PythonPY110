"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls.py import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls.py'))
"""
from random import random

from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include

from app_datetime.views import datetime_view        # ПОСЛЕ ИСПОЛЬЗОВАНИЯ INCLUDE (отдеельных файлов urls из приложений)
from app_weather.views import my_weather_view       # ЭТИ ПРЕДСТАВЛЕНИЯ (вьюхи) СТАНОВЯТСЯ НЕЗАДЕЙСТВОВАННЫМИ
from store.views import products_view, shop_view    # И ОКРАШИВАЮТСЯ СЕРЫМ


def random_view(request):                   # ПИСАТЬ ПРЕДСТАВЛЕНИЯ (вьюхи) МОЖНО И ВНУТРИ ФАЙЛА URLS
    if request.method == "GET":             # ТОГДА ИХ НЕ НАДО ИМПОРТИРОВАТЬ
        return HttpResponse(random())       # НО ЭТО НЕ ЛУЧШАЯ ПРАКТИКА

urlpatterns = [
    path('admin/', admin.site.urls),        # TODO НАЙТИ ГДЕ ЛЕЖИТ ЭТОТ ФАЙЛ И ЧЕМ ОН ЯВЛЯЕТСЯ - VIEWS ИЛИ URLS
    path('random/', random_view),           # ПРЕДСТАВЛЕНИЕ (вьюха) В ТАКОМ СЛУЧАЕ ДОЛЖНА БЫТЬ ВЫШЕ

    #path('datetime/', datetime_view),
    path('', include('app_datetime.urls')),     # ВКЛЮЧЕНИЕ ПУТЕЙ ИЗ ОТДЕЛЬНОГО ФАЙЛА (urls.py) В ПРИЛОЖЕНИИ "app_datetime"

    # path('weather/', my_weather_view),
    path('', include('app_weather.urls')),      # ВКЛЮЧЕНИЕ ПУТЕЙ ИЗ ОТДЕЛЬНОГО ФАЙЛА (urls.py) В ПРИЛОЖЕНИИ "app_weather"

    # path('product/', products_view),
    # path('', shop_view)
    path('', include('store.urls'))             # ВКЛЮЧЕНИЕ ПУТЕЙ ИЗ ОТДЕЛЬНОГО ФАЙЛА (urls.py) В ПРИЛОЖЕНИИ "store"

]
