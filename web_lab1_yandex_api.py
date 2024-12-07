import requests
import json
from datetime import datetime
#import datetime  #разобраться почему при импорте всей библиотеки целиком метод "fromtimestamp" не работает

def current_weather_from_yandex_api(lat, lon):
    """
    Функция для определения текущей погоды по введённым координатам
    :param lat: широта
    :param lon: долгота
    :return: Краткая сводка о текущей погоде
    """
    token = '34d88ba1-ba36-4973-b559-446eca0a920f'
    headers = {'X-Yandex-Weather-Key': token}
    #lat, lon = 59.93, 30.31
    response = requests.get(f'https://api.weather.yandex.ru/v2/forecast?{lat}&{lon}', headers=headers)
    wind_direction_transform = {
        'n': 'северное',                        'e': 'восточное',
        's': 'южное',                           'w': 'западное',
        'ne': 'северо - восточное',             'se': 'юго - восточное',
        'sw': 'юго - западное',                 'nw': 'северо - западное',
        'nne': 'северо - северо - восточное',   'ene': 'восточно - северо - восточное',
        'nnw': 'северо - северо - западное',    'wnw': 'западно - северо - западное',
        'sse': 'юго - юго - восточное',         'ese': 'восточно - юго - восточное',
        'ssw': 'юго - юго - западное',          'wsw': 'западно - юго - западное',
        'c': 'штиль' }
    data = response.json()
    result = {
        'ГОРОД': data['info']['tzinfo']['name'],
        # 'КОГДА_': data['now_dt'], # первоначальный вариант
        'КОГДА': datetime.fromtimestamp(data['fact']['uptime']).strftime("%H:%M"),
        'ТЕМПЕРАТУРА': data['fact']['temp'],
        'ТЕМПЕРАТУРА_ОЩУЩАЕМАЯ': data['fact']['feels_like'],
        'ДАВЛЕНИЕ': data['fact']['pressure_mm'],
        'ВЛАЖНОСТЬ': data['fact']['humidity'],
        'СКОРОСТЬ_ВЕТРА': data['fact']['wind_speed'],
        'ПОРЫВЫ ВЕТРА': data['fact']['wind_gust'],
        #'НАПРАВЛЕНИЕ ВЕТРА_': data['fact']['wind_dir'] # первоначальный вариант
        'НАПРАВЛЕНИЕ ВЕТРА': wind_direction_transform.get(data['fact']['wind_dir'])     # возвращает значение по ключу
    }
    # print(json.dumps(data, indent=4))
    return result



if __name__ == "__main__":
    print(current_weather_from_yandex_api(59.93, 30.31))  # Проверка работы для координат Санкт-Петербурга
