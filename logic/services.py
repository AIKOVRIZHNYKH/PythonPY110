import os, json
from store.models import DATABASE


def filtering_category(database: dict[str, dict],
                       category_key: [None, str] = None,
                       ordering_key: [None, str] = None,
                       reverse: bool = False):
    """
    Функция фильтрации данных по параметрам

    :param database: База данных. (словарь словарей. При проверке в качестве database будет передаваться словарь DATABASE из models.py)
    :param category_key: [Опционально] Ключ для группировки категории. Если нет ключа, то рассматриваются все товары.
    :param ordering_key: [Опционально] Ключ по которому будет произведена сортировка результата.
    :param reverse: [Опционально] Выбор направления сортировки:
        False - сортировка по возрастанию;
        True - сортировка по убыванию.
    :return: list[dict] список товаров с их характеристиками, попавших под условия фильтрации. Если нет таких элементов,
    то возвращается пустой список
    """
    if category_key is not None:
        result = [prod for prod in DATABASE.values() if prod['category'] == category_key]  # TODO При помощи фильтрации в list comprehension профильтруйте товары по категории (ключ 'category') в продукте database. Или можете использовать
        # обычный цикл или функцию filter. Допустим фильтрацию в list comprehension можно сделать по следующему шаблону
        # [product for product in database.values() if ...] подумать, что за фильтрующее условие можно применить.
        # Сравните значение категории продукта со значением category_key
    else:
        result = [prod for prod in DATABASE.values()]  # TODO Трансформируйте словарь словарей database в список словарей
        # В итоге должен быть [dict, dict, dict, ...], где dict - словарь продукта из database
    if ordering_key is not None:
        result.sort(key=lambda x: x.get(ordering_key), reverse=reverse)  # TODO Проведите сортировку result по ordering_key и параметру reverse
        # Так как result будет списком, то можно применить метод sort, но нужно определиться с тем по какому элементу сортируем и в каком направлении
        # result.sort(key=lambda ..., reverse=reverse)
        # Вспомните как можно сортировать по значениям словаря при помощи lambda функции
    return result


def view_in_cart() -> dict:  # Уже реализовано, не нужно здесь ничего писать
    """
    Просматривает содержимое cart.json
    :return: Содержимое 'cart.json'
    """
    if os.path.exists('cart.json'):  # Если файл существует
        with open('cart.json', encoding='utf-8') as f:
            return json.load(f)
    cart = {'products': {}}  # Создаём пустую корзину
    with open('cart.json', mode='x', encoding='utf-8') as f:   # Создаём файл и записываем туда пустую корзину
        json.dump(cart, f)
    return cart


def add_to_cart(id_product: str) -> bool:
    """
    Добавляет продукт в корзину. Если в корзине нет данного продукта,
    то добавляет его с количеством равное 1.
    Если в корзине есть такой продукт, то добавляет количеству данного продукта + 1.
    :param id_product: Идентификационный номер продукта в виде строки.
    :return: Возвращает True в случае успешного добавления,
    а False в случае неуспешного добавления (товара по id_product не существует).
    """
    cart = view_in_cart()   # json с корзиной товаров (питоновский словарь)
    # if id_product in cart['products'] and id_product in DATABASE:
    #     cart['products'][id_product] += 1
    #     with open('cart.json', mode='w', encoding='utf-8') as f:
    #         json.dump(cart, f)
    #     return True
    # elif id_product not in cart['products'] and id_product in DATABASE:
    #     cart['product'][id_product] = 1
    #     with open('cart.json', mode='w', encoding='utf-8') as f:
    #         json.dump(cart, f)
    #     return True
    # else:
    #     return False
    if id_product in DATABASE:
        if id_product in cart['products']:
            cart['products'][id_product] += 1
            #TODO надо разобраться почему фактически добавляется по 2 штуке за раз, а не по 1 штуке
        else:
            cart['products'][id_product] = 1
        with open('cart.json', mode='w', encoding='utf-8') as f:
            json.dump(cart, f)
        return True
    return False


def remove_from_cart(id_product: str) -> bool:
    """
    Добавляет позицию продукта из корзины.
    Если в корзине есть такой продукт, то удаляется ключ в словаре с этим продуктом.
    :param id_product: Идентификационный номер продукта в виде строки.
    :return: Возвращает True в случае успешного удаления,
    а False в случае неуспешного удаления(товара по id_product не существует).
    """
    cart = view_in_cart()
    if id_product not in cart['products']:
        return False
    cart['products'].pop(id_product)
    with open('cart.json', mode='w', encoding='utf-8') as f:
        json.dump(cart, f)
    return True




if __name__ == "__main__":
    from store.models import DATABASE

    test = [
        {'name': 'Клубника', 'discount': None, 'price_before': 500.0,
         'price_after': 500.0,
         'description': 'Сладкая и ароматная клубника, полная витаминов, чтобы сделать ваш день ярче.',
         'rating': 5.0, 'review': 200, 'sold_value': 700,
         'weight_in_stock': 400,
         'category': 'Фрукты', 'id': 2, 'url': 'store/images/product-2.jpg',
         'html': 'strawberry'},

        {'name': 'Яблоки', 'discount': None, 'price_before': 130.0,
         'price_after': 130.0,
         'description': 'Сочные и сладкие яблоки - идеальная закуска для здорового перекуса.',
         'rating': 4.7, 'review': 30, 'sold_value': 70, 'weight_in_stock': 200,
         'category': 'Фрукты', 'id': 10, 'url': 'store/images/product-10.jpg',
         'html': 'apple'}
    ]

    print(filtering_category(DATABASE, 'Фрукты', 'price_after', True) == test)  # True



