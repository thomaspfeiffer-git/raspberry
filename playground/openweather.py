#!/usr/bin/python3

# weather icons:
# https://openweathermap.org/weather-conditions

import json
import pprint
from urllib.request import urlopen

# SensorValue:
#    each value gets its own SensorValue() instance
#    compare to BME280: gets three instances of SensorValues in its constructor

# provide api:
# http://flask-restful.readthedocs.io/en/latest/quickstart.html#a-minimal-api


def read_api_key ():
    with open("openweathermap.key", "r") as key_file:
        return key_file.read().rstrip() 

def owm_url ():
    base_url = "http://api.openweathermap.org/data/2.5/forecast"
    location = "vienna,at"
    appid    = read_api_key()
    units    = "metric"
    lang     = "de"
    return "{}?q={}&APPID={}&units={}&lang={}".format(base_url, location, \
                                                      appid, units, lang)


def make_icon_url (icon):
    path_to_icons = "http://openweathermap.org/img/w/"
    extension     = "png"
    return "{}{}.{}".format(path_to_icons, icon, extension)


def get_noon_id (owm_data):
    i = 0
    while "12:00:00" not in owm_data[i]['dt_txt']:
        i += 1 
    return i


response = urlopen(owm_url())
data = json.loads(response.read().decode("utf-8"))
forecast_owm = data['list'][get_noon_id(data['list'])]

forecast = {
            'temp':  forecast_owm['main']['temp'],
            'humidity': forecast_owm['main']['humidity'],
            'wind': forecast_owm['wind']['speed'],
            'desc': forecast_owm['weather'][0]['description'],
            'icon_url': make_icon_url(forecast_owm['weather'][0]['icon']),
            'time': forecast_owm['dt'],
            'time_text': forecast_owm['dt_txt']
           }


pprint.pprint(forecast)

# eof #

