from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from store.models import DATABASE
from logic.services import filtering_category, view_in_cart, add_to_cart, remove_from_cart


# Create your views here.
def products_view(request):
    if request.method == "GET":
        id_ = request.GET.get('id')     # GET - это тип запроса, а get это метод получающий значение по ключу id
        if id_:                         # если запрошенный id-шник существует
            if id_ in DATABASE:         # и если запрошенный id-шник имеется в БАЗЕ (см. models.py)
                return JsonResponse(DATABASE.get(id_), json_dumps_params={'ensure_ascii':False, 'indent':4})
            return HttpResponseNotFound("ДАННОГО ПРОДУКТА НЕТ В БАЗЕ ДАННЫХ")
        category_key = request.GET.get('category')
        ordering_key = request.GET.get('ordering')
        reverse_key = request.GET.get('reverse')
        if ordering_key:
            if str(reverse_key).lower() == 'true':
                data = filtering_category(DATABASE, category_key, ordering_key, True)
                # ТЕСТОВАЯ ССЫЛКА http://127.0.0.1:8000/product/?category=%D0%9E%D0%B2%D0%BE%D1%89%D0%B8&ordering=rating&reverse=True
            else:
                data = filtering_category(DATABASE, category_key, ordering_key)
                # ТЕСТОВАЯ ССЫЛКА http://127.0.0.1:8000/product/?category=%D0%9E%D0%B2%D0%BE%D1%89%D0%B8&ordering=rating
        else:
            data = filtering_category(DATABASE, category_key)
            # ТЕСТОВАЯ ССЫЛКА http://127.0.0.1:8000/product/?category=%D0%9E%D0%B2%D0%BE%D1%89%D0%B8
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii':False, 'indent':4})

def shop_view(request):
    if request.method == "GET":
        # with open('store/shop.html', 'r', encoding='utf-8') as f:
        #     data = f.read()
        # return HttpResponse(data)
        return render(request, 'store/shop.html', context={'products': DATABASE.values()})

def products_page_view(request, page):
    if request.method == "GET":
        if isinstance(page, str):
            for prod in DATABASE.values():
                if prod['html'] == page:
                    with open(f'store/products/{page}.html', encoding='utf-8') as f:
                        data = f.read()
                    return HttpResponse(data)
        elif isinstance(page, int):
            prod = DATABASE.get(str(page))      # словарь с ВЫБРАННЫМ по строковому номеру продукту
            if prod:
                with open(f'store/products/{prod["html"]}.html', encoding='utf-8') as f:
                    data = f.read()
                return HttpResponse(data)
        return HttpResponseNotFound("ПРОДУКТА НЕ СУЩЕСТВУЕТ")

def cart_view(request):
    if request.method == "GET":
        data = view_in_cart()
        format_for_result = request.GET.get('format')
        if format_for_result and format_for_result.lower() == 'json':
            return JsonResponse(data, json_dumps_params={'ensure_ascii': False, 'indent': 4})
            # ТЕСТОВАЯ ССЫЛКА http://127.0.0.1:8000/cart/?format=json

        products = []
        for id_prod, count in data.get('products').items():
            product = DATABASE[id_prod]
            product['count'] = count
            product['price_total'] = round(count * product['price_after'], 2)
            products.append(product)

        return render(request, 'store/cart.html', context = {'products': products})

def cart_add_view(request, id_product):
    if request.method == "GET":
        result = add_to_cart(id_product)
        if result:
            return JsonResponse({"answer": "ПРОДУКТ УСПЕШНО ДОБАВЛЕН В КОРЗИНУ"},
                                json_dumps_params={'ensure_ascii': False})
        else:
            return JsonResponse({"answer": "НЕУДАЧНОЕ ДОБАВЛЕНИЕ В КОРЗИНУ"},
                                status=404,
                                json_dumps_params={'ensure_ascii': False})

def cart_del_view(request, id_product):
    if request.method == "GET":
        result = remove_from_cart(id_product)
        if result:
            return JsonResponse({"answer": "ПРОДУКТ УСПЕШНО УБРАН ИЗ КОРЗИНЫ"},
                                json_dumps_params={'ensure_ascii': False})
        else:
            return JsonResponse({"answer": "НЕУДАЧНОЕ УБИРАНИЕ ИЗ КОРЗИНЫ"},
                                status=404,
                                json_dumps_params={'ensure_ascii': False})





