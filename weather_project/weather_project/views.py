import os
import requests
from django.http import JsonResponse
from geopy.geocoders import Nominatim
from django.core.cache import cache


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
        return None

def get_coordinates(city_name):
    geolocator = Nominatim(user_agent="weather_project")
    location = geolocator.geocode(city_name, language="ru")

    if location:
        return location.latitude, location.longitude, location.address.split(',')[0]
    else:
        return None

def process_cache(cache_key):
    cached_data = cache.get(cache_key[2])
    if cached_data:
        return cached_data
    else:
        lat, lon, _ = cache_key
        cached_data = get_weather(lat, lon)
        cache.set(cache_key, cached_data, 1800)
        return cached_data

def test_cache(cache_key):
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data
    else:
        lat, lon, _ = cache_key
        cached_data = get_weather(lat, lon)
        cache.set(cache_key, cached_data, 1800)
        return cached_data

def get_bot_status():
    response = requests.get("http://bot:7772/get_status")
    return response.text

def weather(request):
    city = request.GET.get('city', '')
    resault = get_coordinates(city)
    if not resault:
        return JsonResponse({'NameCityError': 'City not found'})
    cached_data = process_cache(resault)

    temp = cached_data['temp']
    pressure = cached_data['pressure_mm']
    wind_speed = cached_data['wind_speed']

    return JsonResponse({'temperature': temp, 'pressure': pressure, 'wind_speed': wind_speed})

def forecasts(request):
    city = request.GET.get('city', '')
    resault = get_coordinates(city)
    if not resault:
        return JsonResponse({'NameCityError': 'City not found'})
    cached_data = process_cache(resault)
    return JsonResponse({'forecasts': cached_data['forecasts']})