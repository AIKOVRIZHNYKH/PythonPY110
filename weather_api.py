import requests
from datetime import datetime



def current_weather_from_api(city):
    token = "86e6f03643fc4ac294d113732243011"
    url = f"https://api.weatherapi.com/v1/current.json?key={token}]&q={city}"
    response = requests.get(url)
    print(response.text)


# Словарь перевода значений направления ветра
DIRECTION_TRANSFORM = {
    'n': 'северное',
    'nne': 'северо - северо - восточное',
    'ne': 'северо - восточное',
    'ene': 'восточно - северо - восточное',
    'e': 'восточное',
    'ese': 'восточно - юго - восточное',
    'se': 'юго - восточное',
    'sse': 'юго - юго - восточное',
    's': 'южное',
    'ssw': 'юго - юго - западное',
    'sw': 'юго - западное',
    'wsw': 'западно - юго - западное',
    'w': 'западное',
    'wnw': 'западно - северо - западное',
    'nw': 'северо - западное',
    'nnw': 'северо - северо - западное',
    'c': 'штиль',
}


def current_weather(lat, lon):
    """
    Описание функции, входных и выходных переменных
    """
    token = '34d88ba1-ba36-4973-b559-446eca0a920f'  # Вставить ваш токен
    url = f"https://api.weather.yandex.ru/v2/forecast?lat={lat}&lon={lon}"  # Если вдруг используете тариф «Погода на вашем сайте»
    # то вместо forecast используйте informers. url = f"https://api.weather.yandex.ru/v2/informers?lat={lat}&lon={lon}"
    headers = {"X-Yandex-API-Key": f"{token}"}
    response = requests.get(url, headers=headers)
    data = response.json()

    # Данная реализация приведена для тарифа «Тестовый», если у вас Тариф «Погода на вашем сайте», то закомментируйте пару строк указанных ниже
    result = {
        'city': data['geo_object']['locality']['name'],  # Если используете Тариф «Погода на вашем сайте», то закомментируйте эту строку
        'time': datetime.fromtimestamp(data['fact']['uptime']).strftime("%H:%M"),  # Если используете Тариф «Погода на вашем сайте», то закомментируйте эту строку
        #'temp': 'реализация',  # TODO Реализовать вычисление температуры из данных полученных от API
        #'feels_like_temp': 'реализация',  # TODO Реализовать вычисление ощущаемой температуры из данных полученных от API
        #'pressure': 'реализация',  # TODO Реализовать вычисление давления из данных полученных от API
        #'humidity': 'реализация',  # TODO Реализовать вычисление влажности из данных полученных от API
        #'wind_speed': 'реализация',  # TODO Реализовать вычисление скорости ветра из данных полученных от API
        #'wind_gust': 'реализация',  # TODO Реализовать вычисление скорости порывов ветка из данных полученных от API
        'wind_dir': DIRECTION_TRANSFORM.get(data['fact']['wind_dir']),  # Если используете Тариф «Погода на вашем сайте», то закомментируйте эту строку
    }
    return result


if __name__ == "__main__":
    print(current_weather(59.93, 30.31))  # Проверка работы для координат Санкт-Петербурга


