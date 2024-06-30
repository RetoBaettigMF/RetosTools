import requests
import json
import os
from datetime import datetime, timedelta

API_URL = 'https://wttr.in/Uster?format=%C %t'
CACHE_FILE = 'weather_cache.json'
CACHE_DURATION = timedelta(hours=1)


def fetch_weather():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.text
    else:
        return None


def save_cache(data):
    with open(CACHE_FILE, 'w') as f:
        json.dump(data, f)


def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            return json.load(f)
    return None


if __name__ == '__main__':
    cache = load_cache()
    now = datetime.now()

    if cache:
        cached_time = datetime.fromisoformat(cache['timestamp'])
        if now - cached_time < CACHE_DURATION:
            print('Loaded data from cache:')
            print(cache['weather'])
        else:
            weather = fetch_weather()
            if weather:
                print('Fetched new data:')
                print(weather)
                save_cache({'timestamp': now.isoformat(), 'weather': weather})
            else:
                print('Error fetching weather data.')
    else:
        weather = fetch_weather()
        if weather:
            print('Fetched new data:')
            print(weather)
            save_cache({'timestamp': now.isoformat(), 'weather': weather})
        else:
            print('Error fetching weather data.')