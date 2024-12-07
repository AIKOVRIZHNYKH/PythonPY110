import requests

def current_weather_from_api(city):
    token = "86e6f03643fc4ac294d113732243011"
    url = f"https://api.weatherapi.com/v1/current.json?key={token}&q={city}"
    response = requests.get(url)
    print(response.text)


if __name__ == "__main__":
    current_weather_from_api("Saint-Petersburg")