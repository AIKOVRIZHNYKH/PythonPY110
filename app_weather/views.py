from django.http import JsonResponse
from django.shortcuts import render

# ОБТАТИТЬ ВНИМАНИЕ ЧТО ИСПОЛЬЗОВАН ОТДЕЛЬНЫЙ МОДУЛЬ, ТОЛЬКО  ПРО api.weatherapi.com, БЕЗ ХВОСТОВ ПРО API ОТ ЯНДЕКСА
from web_lab1_weather_api import current_weather_from_api

def my_weather_view(request):
    if request.method == "GET":
        data = current_weather_from_api('Saint-Petersburg')
        return JsonResponse(data, json_dumps_params={'ensure_ascii':False, 'indent':4}, safe=False)

