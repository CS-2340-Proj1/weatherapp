# weather/views.py
import datetime
import requests
from django.shortcuts import render
from django.conf import settings


def index(request):
    weather_data = None
    error_message = None
    zip_code = request.GET.get('zip_code')
    unit = request.GET.get('unit', 'imperial')  # imperial for Fahrenheit, metric for Celsius

    if zip_code:
        api_key = settings.WEATHER_API_KEY
        url = f"http://api.openweathermap.org/data/2.5/weather?zip={zip_code},us&appid={api_key}&units={unit}"
        response = requests.get(url)
        if response.status_code == 200:
            weather_data = response.json()
            lat = weather_data['coord']['lat']
            lon = weather_data['coord']['lon']
            # The API returns 'dt' (timestamp) and 'timezone' (offset in seconds from UTC)
            # We'll pass these along for our dynamic displays.
        else:
            error_message = "Error fetching weather data. Please check the zip code and try again."

    context = {
        'weather_data': weather_data,
        'error_message': error_message,
        'unit': unit,
        'zip_code': zip_code,
        'lat': weather_data['coord']['lat'] if weather_data else None,
        'lon': weather_data['coord']['lon'] if weather_data else None,
        'owm_key': settings.WEATHER_API_KEY,  # reuse same key
    }
    return render(request, 'weather/index.html', context)
