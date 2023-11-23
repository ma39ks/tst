import os
import requests
from django.http import JsonResponse
from geopy.geocoders import Nominatim
from django.core.cache import cache
import json


# def get_weather(lat: float, lon: float) -> JsonResponse:
# def get_weather() -> JsonResponse:
#     # h = {
#     #     'X-Yandex-API-Key': os.environ.get('YaWeatherKey')
#     # }
#     # response = requests.get(f'https://api.weather.yandex.ru/v2/forecast/?lat={lat}&lon={lon}&lang=ru_RU', headers=h)
#     # data = response.json()
#     with open('example_req.json', 'r') as f:
#         data = json.load(f)
#     return {
#         'temp': data['fact']['temp'], 
#         'pressure_mm': data['fact']['pressure_mm'],
#         'wind_speed': data['fact']['wind_speed'],
#         'forecasts': {
#             'night_short': {
#                 'temp': data['forecasts'][0]['parts']['night_short']['temp'],
#                 'pressure_mm': data['forecasts'][0]['parts']['night_short']['pressure_mm'],
#                 'wind_speed': data['forecasts'][0]['parts']['night_short']['wind_speed'],
#                 },
#             'day_short': {
#                 'temp': data['forecasts'][0]['parts']['day_short']['temp'],
#                 'pressure_mm': data['forecasts'][0]['parts']['day_short']['pressure_mm'],
#                 'wind_speed': data['forecasts'][0]['parts']['day_short']['wind_speed'],
#                 },
#         },
#         }

def get_coordinates(city_name):
    geolocator = Nominatim(user_agent="weather_project")
    location = geolocator.geocode(city_name, language="ru")

    if location:
        return location.latitude, location.longitude, location.address.split(',')[0]
    else:
        print(f"Координаты для города {city_name} не найдены.")
        return None

def get_weather(lat: float, lon: float) -> JsonResponse:
    h = {
        'X-Yandex-API-Key': os.environ.get('YaWeatherKey')
    }
    response = requests.get(f'https://api.weather.yandex.ru/v2/forecast/', headers=h,
    params={
        'lat': lat,
        'lon': lon,
        'lang': 'ru_RU'
    })
    print(response)
    if response.status_code == 200:
        data = response.json()
        return {
            'temp': data['fact']['temp'], 
            'pressure_mm': data['fact']['pressure_mm'],
            'wind_speed': data['fact']['wind_speed'],
            'forecasts': {
                'night_short': {
                    'temp': data['forecasts'][0]['parts']['night_short']['temp'],
                    'pressure_mm': data['forecasts'][0]['parts']['night_short']['pressure_mm'],
                    'wind_speed': data['forecasts'][0]['parts']['night_short']['wind_speed'],
                    },
                'day_short': {
                    'temp': data['forecasts'][0]['parts']['day_short']['temp'],
                    'pressure_mm': data['forecasts'][0]['parts']['day_short']['pressure_mm'],
                    'wind_speed': data['forecasts'][0]['parts']['day_short']['wind_speed'],
                    },
            },
            }
    else:
        return response.status_code

# print(get_coordinates('Нижний Новгород'))
print(get_weather(56.326799, 44.00652))

# def weather(request):
#     city = request.GET.get('city', '')
#     print(city)
#     cache_key = f'weather_{city}'

#     # Проверяем кэш
#     cached_data = cache.get(cache_key)
#     if cached_data:
#         temp, pressure, wind_speed = cached_data
#     else:
#         # Получаем координаты города через OpenStreetMap (замените на свою реализацию)
#         # Здесь можно использовать библиотеку geopy
#         lat, lon = get_coordinates(city)
#         temp, pressure, wind_speed = get_weather(lat, lon)

#         # Кэшируем данные на 30 минут
#         cache.set(cache_key, (temp, pressure, wind_speed), 1800)

#     return JsonResponse({'temperature': temp, 'pressure': pressure, 'wind_speed': wind_speed})
