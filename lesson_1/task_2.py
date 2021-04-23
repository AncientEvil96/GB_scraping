# Зарегистрироваться на https://openweathermap.org/api и написать функцию,
# которая получает погоду в данный момент для города,
# название которого получается через input. https://openweathermap.org/current

import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()


class Weather:
    def __init__(self, appid):
        self._appid = appid

    def get_by_city_name(self, city):
        params = {
            'q': city,
            'appid': self._appid
        }
        url = 'https://api.openweathermap.org/data/2.5/weather'
        repos_r = requests.get(url, params=params)
        return repos_r.json()

    def save_to_file(self, file_name, data):
        with open(f'{file_name}.json', 'w') as f:
            json.dump(data, f)


if __name__ == '__main__':
    appid = os.environ.get('appid_weather', None)
    weather = Weather(appid)
    object_json = weather.get_by_city_name('N_C_W', 'Naberezhnye Chelny')
    weather.save_to_file(object_json)
