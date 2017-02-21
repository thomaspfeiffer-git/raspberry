#!/usr/bin/python3

# weather icons:
# https://openweathermap.org/weather-conditions

import json
import pprint
import threading
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


class OpenWeatherMap_Config (object):
    """ todo """
    def read_api_key ():
        with open("openweathermap.key", "r") as key_file:
            return key_file.read().rstrip() 

    _base_url = "http://api.openweathermap.org/data/2.5/"
    _api_key  = read_api_key()
    _location = "vienna,at"
    _units    = "metric"
    _lang     = "de"

    _path_to_icons = "http://openweathermap.org/img/w/"
    _extension     = "png"

    _url = "{}{{}}?q={}&APPID={}&units={}&lang={}".format(                      
            _base_url, _location, _api_key, _units, _lang)
    url_forecast = _url.format("forecast")
    url_actual   = _url.format("weather")

    @classmethod
    def icon_url (cls, icon):
        return "{0._path_to_icons}{1}.{0._extension}".format(cls, icon)

    """TODO: prevent from instantiating"""


class OpenWeatherMap_Data (threading.Thread):
    """ todo """
    def __init__ (self):
        self.__lock = threading.Lock()

        self.__forecast = []
        self.__weather  = {}

        self.__running = True

    def __str__ (self):
        pass

    def read_data (self):
        response = urlopen(OpenWeatherMap_Config.url_forecast)
        data = json.loads(response.read().decode("utf-8"))

        # get data from 12:00 am only
        forecast_owm = [ data['list'][i] 
                         for i in range(len(data['list'])) 
                         if "12:00:00" in data['list'][i]['dt_txt'] ]

        with self.__lock:
            self.__forecast = []
            for i in range(len(forecast_owm)):
                self.__forecast.append({
                     'temp':  forecast_owm[i]['main']['temp'],
                     'humidity': forecast_owm[i]['main']['humidity'],
                     'wind': forecast_owm[i]['wind']['speed'],
                     'desc': forecast_owm[i]['weather'][0]['description'],
                     'icon_url': make_icon_url(forecast_owm[i]['weather'][0]['icon']),
                     'time': forecast_owm[i]['dt'],
                     'time_text': forecast_owm[i]['dt_txt']
                    })


        with self.__lock:
            pass
            # self.__weather = ...

    @property
    def forecast (self):
        with self.__lock:
            pass
            # return shallow copy 

    @property
    def weather (self):
        with self.__lock:
            pass
            # return shallow copy 


    def run (self):
        while self.__running:
            pass
            # interruptible sleep!

    def stop (self):
        self.__running = False






ooooo = OpenWeatherMap_Data()

"""


pprint.pprint(forecast)


if __name__ == '__main__':
    app.run()
"""


# eof #

