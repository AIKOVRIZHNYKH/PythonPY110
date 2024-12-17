from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from store.models import DATABASE


# Create your views here.
def products_view(request):
    if request.method == "GET":
        id_ = request.GET.get('id')     # GET - это тип запроса, а get это метод получающий значение по ключу id
        if id_:                         # если запрошенный id-шник существует
            if id_ in DATABASE:         # и если запрошенный id-шник имеется в БАЗЕ (см. models.py)
                return JsonResponse(DATABASE.get(id_), json_dumps_params={'ensure_ascii':False, 'indent':4})
            return HttpResponseNotFound("ДАННОГО ПРОДУКТА НЕТ В БАЗЕ ДАННЫХ")
        return JsonResponse(DATABASE, json_dumps_params={'ensure_ascii':False, 'indent':4})

def shop_view(request):
    if request.method == "GET":
        with open('store/shop.html', 'r', encoding='utf-8') as f:
            data = f.read()
        return HttpResponse(data)



