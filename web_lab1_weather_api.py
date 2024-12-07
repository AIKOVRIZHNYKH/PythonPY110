import json
from datetime import datetime

import requests

def current_weather_from_api(city):
    token = "86e6f03643fc4ac294d113732243011"
    parameters = {'key':token, 'q':city}
    #url = f"https://api.weatherapi.com/v1/current.json?key={token}&q={city}"
    url = f"https://api.weatherapi.com/v1/current.json"
    response = requests.get(url, params=parameters)
    #print(response.text)
    data = response.json()
    #print(json.dumps(data, indent=4))
    result = {
        "ГОРОД": data['location']['name'],
        "СТРАНА": data['location']['country'],
        "ТЕМПЕРАТУРА_ГРАД_ЦЕЛЬС": data['current']['temp_c'],
        "ТЕМПЕРАТУРА_ОЩУЩАЕМАЯ": data['current']['feelslike_c'],
        "ВЕТЕР_КМ_Ч": data['current']['wind_kph'],
        "КОГДА": data['current']['last_updated']
        #"КОГДА": datetime.fromisoformat(data['current']['last_updated']) # TODO РАЗОБРАТЬСЯ ПОЧЕМУ НЕ РАБОТАЕТ
    }
    result_json = json.dumps(result, ensure_ascii=False, indent=4)      # dumps записывает в строку формата json
    #print(result_json)
    return result








if __name__ == "__main__":
    current_weather_from_api("Saint-Petersburg")