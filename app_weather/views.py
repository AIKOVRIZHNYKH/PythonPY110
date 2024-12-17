from django.http import JsonResponse
from django.shortcuts import render

# ОБРАТИТЬ ВНИМАНИЕ ЧТО ИСПОЛЬЗОВАН ОТДЕЛЬНЫЙ МОДУЛЬ,
# ТОЛЬКО  ПРО api.weatherapi.com, БЕЗ ХВОСТОВ ПРО API ОТ ЯНДЕКСА
from web_lab1_weather_api import current_weather_from_api


# РЕЗЕРВНАЯ КОПИЯ (ДО ИЗМЕНЕНИЯ 17.12.2024)
#def my_weather_view(request):
    #if request.method == "GET":
        #data = current_weather_from_api('Saint-Petersburg')
        #return JsonResponse(data, json_dumps_params={'ensure_ascii':False, 'indent':4}, safe=False)

def my_weather_view(request):
    if request.method == "GET":
        town = request.GET.get('city')      # протестировать можно на http://127.0.0.1:8000/weather/?city=Moscow
        if town:
            data = current_weather_from_api(town)
        else:
            data = current_weather_from_api('Saint-Petersburg')
        return JsonResponse(data, json_dumps_params={'ensure_ascii':False, 'indent':4}, safe=False)



