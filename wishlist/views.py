from django.contrib.auth import get_user
from django.http import JsonResponse, HttpResponseNotFound
from django.shortcuts import render, redirect

from logic.services import view_in_wishlist, add_to_wishlist, remove_from_wishlist
from store.models import DATABASE
from django.contrib.auth.decorators import login_required


@login_required(login_url='login:login_view')
def wishlist_view(request):
    if request.method == "GET":
        # Имя текущего пользователя
        current_user = get_user(request).username
        # Словарь вида {'products': []} со списком айдишников избранного текущего пользователя
        data = view_in_wishlist(request)[current_user]

        products = []   # Заготовка для списка словарей продуктов с их характеристиками

        for id_prod in data['products']:    # Для каждого элемента списка айдишников избранного
            product = DATABASE[id_prod]     # Берём словарь со всеми характеристиками продукта из Базы данных
            products.append(product)        # И сохраняем этот словарь в список словарей

        return render(request, 'wishlist/wishlist.html',
                      context={'products': products})


@login_required(login_url='login:login_view')
def wishlist_add_json(request, id_product: str):
    """
    Добавление продукта в избранное и возвращение информации об успехе или неудаче в JSON
    :param request: ...
    :param id_product: ...
    :return: ...
    """
    if request.method == "GET":
        # result = add_to_cart(id_product)
        result = add_to_wishlist(request, id_product)
        if result:
            return JsonResponse({"answer": "ПРОДУКТ УСПЕШНО ДОБАВЛЕН В ИЗБРАННОЕ"},
                                json_dumps_params={'ensure_ascii': False})
        else:
            return JsonResponse({"answer": "НЕУДАЧНОЕ ДОБАВЛЕНИЕ В ИЗБРАННОЕ"},
                                status=404,
                                json_dumps_params={'ensure_ascii': False})

@login_required(login_url='login:login_view')
def wishlist_del_json(request, id_product: str):
    if request.method == "GET":
        # result = remove_from_cart(id_product)
        result = remove_from_wishlist(request, id_product)
        if result:
            return JsonResponse({"answer": "ПРОДУКТ УСПЕШНО УБРАН ИЗ ИЗБРАННОГО"},
                                json_dumps_params={'ensure_ascii': False})
        else:
            return JsonResponse({"answer": "НЕУДАЧНОЕ УДАЛЕНИЕ ИЗ ИЗБРАННОГО"},
                                status=404,
                                json_dumps_params={'ensure_ascii': False})

@login_required(login_url='login:login_view')
def wishlist_json(request):
    """
    Просмотр всех продуктов в избранном для пользователя и возвращение этого в JSON
    """
    if request.method == "GET":
        # Имя текущего пользователя
        current_user = get_user(request).username
        # Словарь вида {'products': []} со списком айдишников избранного текущего пользователя
        data = view_in_wishlist(request)[current_user]
        if data:
            return JsonResponse(data,
                                json_dumps_params={'ensure_ascii': False,
                                                   'indent': 4})
        return JsonResponse({"answer": "ПОЛЬЗОВАТЕЛЬ НЕ АВТОРИЗОВАН"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})


def wishlist_remove_view(request, id_product):
    if request.method == "GET":
        # result = remove_from_cart(id_product)
        result = remove_from_wishlist(request, id_product)
        if result:
            return redirect('wishlist:wishlist_view')
        return HttpResponseNotFound("НЕУДАЧНОЕ УДАЛЕНИЕ ПРОДУКТА ИЗ ИЗБРАННОГО")



