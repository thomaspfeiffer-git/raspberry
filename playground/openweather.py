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

# install
# sudo pip3 install flask-restful


from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class API_OpenWeatherData (Resource):
    def get (self):
        return json.dumps(forecast)

api.add_resource(API_OpenWeatherData, '/')



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


response = urlopen(owm_url())
data = json.loads(response.read().decode("utf-8"))

# get data from 12:00 only
forecast_owm = [ data['list'][i] for i in range(len(data['list'])) 
                                 if "12:00:00" in data['list'][i]['dt_txt'] ]


forecast = []
for i in range(len(forecast_owm)):
    forecast.append({
                     'temp':  forecast_owm[i]['main']['temp'],
                     'humidity': forecast_owm[i]['main']['humidity'],
                     'wind': forecast_owm[i]['wind']['speed'],
                     'desc': forecast_owm[i]['weather'][0]['description'],
                     'icon_url': make_icon_url(forecast_owm[i]['weather'][0]['icon']),
                     'time': forecast_owm[i]['dt'],
                     'time_text': forecast_owm[i]['dt_txt']
                    })

pprint.pprint(forecast)


if __name__ == '__main__':
    app.run()


# eof #

