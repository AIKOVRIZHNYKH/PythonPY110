from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
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


@login_required(login_url='login:login_view')
def cart_view(request):
    if request.method == "GET":
        # data = view_in_cart()

        current_user = get_user(request).username
        data = view_in_cart(request)[current_user]

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

        return render(request, 'store/cart.html', context={'products': products})


@login_required(login_url='login:login_view')
def cart_add_view(request, id_product):
    if request.method == "GET":
        # result = add_to_cart(id_product)
        result = add_to_cart(request, id_product)
        if result:
            return JsonResponse({"answer": "ПРОДУКТ УСПЕШНО ДОБАВЛЕН В КОРЗИНУ"},
                                json_dumps_params={'ensure_ascii': False})
        else:
            return JsonResponse({"answer": "НЕУДАЧНОЕ ДОБАВЛЕНИЕ В КОРЗИНУ"},
                                status=404,
                                json_dumps_params={'ensure_ascii': False})

def cart_del_view(request, id_product):
    if request.method == "GET":
        # result = remove_from_cart(id_product)
        result = remove_from_cart(request, id_product)
        if result:
            return JsonResponse({"answer": "ПРОДУКТ УСПЕШНО УБРАН ИЗ КОРЗИНЫ"},
                                json_dumps_params={'ensure_ascii': False})
        else:
            return JsonResponse({"answer": "НЕУДАЧНОЕ УБИРАНИЕ ИЗ КОРЗИНЫ"},
                                status=404,
                                json_dumps_params={'ensure_ascii': False})

def coupon_check_view(request, coupon_code):
    DATA_COUPON = \
        {
        "coupon": {
            "value": 10,
            "is_valid": True},
        "coupon_old": {
            "value": 20,
            "is_valid": False},
        "coupon_new": {
            "value": 30,
            "is_valid": True}
        }
    if request.method == "GET":
        if coupon_code in DATA_COUPON:          # Если запрашиваемый купон есть в списке купонов
            coupon = DATA_COUPON[coupon_code]   # То запоминаем внутренний словарик (с ключами "value" и "is_valid")
            data = {
                "discount": coupon['value'],
                "is_valid": coupon['is_valid']
            }
            return JsonResponse(data)
        return HttpResponseNotFound('НЕВЕРНЫЙ КУПОН')


def delivery_estimate_view(request):
    DATA_PRICE = {
        "Россия": {
            "Москва": {"price": 80},
            "Санкт-Петербург": {"price": 50},
            "fix_price": 100,
        },
        "Беларусь": {
            "Минск": {"price": 150},
            "Брест": {"price": 200},
            "fix_price": 250
        }
    }
    if request.method == "GET":
        data = request.GET
        country = data.get("country")       # Считываем параметр по API
        city = data.get("city")             # Считываем параметр по API
        country_in_data = DATA_PRICE.get(country)   # Словарь со всеми городами указанной страны
        city_in_data = country_in_data.get(city)    # Словарь с ценой доставки в указанный город
        if country_in_data:
            if city_in_data:
                return JsonResponse({"price": city_in_data["price"]})
            return JsonResponse({"price": country_in_data["fix_price"]})
        return HttpResponseNotFound("НЕВЕРНЫЕ ДАННЫЕ")


@login_required(login_url='login:login_view')
def cart_buy_now_view(request, id_product):
    if request.method == "GET":
        # result = add_to_cart(id_product)
        result = add_to_cart(request, id_product)
        if result:
            return redirect('store:cart_view')
        return HttpResponseNotFound("НЕУДАЧНОЕ ДОБАВЛЕНИЕ ТОВАРА")

def cart_remove_view(request, id_product):
    if request.method == "GET":
        # result = remove_from_cart(id_product)
        result = remove_from_cart(request, id_product)
        if result:
            return redirect('store:cart_view')
        return HttpResponseNotFound("НЕУДАЧНОЕ УДАЛЕНИЕ ТОВАРА ИЗ КОРЗИНЫ")

