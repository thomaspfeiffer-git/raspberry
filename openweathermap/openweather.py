#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# openweather.py                                                              #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2017                   #
###############################################################################
"""provides data from openweathermap:
   - to my SensorValueQueue for my weather station
   - as an api
"""

### usage ###
# ./openweather.py > openweather.log 2>&1 &


### setup ###
# sudo pip3 install flask-restful


### additional resources and documentation ###
# openweathermap:
# https://openweathermap.org/api
#
# weather icons:
# https://openweathermap.org/weather-conditions
#
# provide api:
# http://flask-restful.readthedocs.io/en/latest/quickstart.html#a-minimal-api


import copy
from datetime import datetime
import json
import signal
import sys
import threading
import time
from urllib.error import HTTPError
from urllib.request import urlopen

sys.path.append("../libs/")
from SensorQueue import SensorQueueClient_write
from SensorValue import SensorValueLock, SensorValue


from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

###############################################################################
# API_OpenWeatherData #########################################################
class API_OpenWeatherData (Resource):
    def get (self):
        return json.dumps(owm_data.weather)

api.add_resource(API_OpenWeatherData, '/')


###############################################################################
# OpenWeatherMap_Config #######################################################
class OpenWeatherMap_Config (object):
    """provides some configuration and static methods for the
       api call to openweathermap"""
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

    @staticmethod
    def direction (degrees):
        """converts wind direction in degrees (0 .. 360) to text"""
        if degrees is None:
            return "n/a"

        directions = "nord nord-ost ost süd-ost süd süd-west west nord-west nord".split()
        return(directions[int((float(degrees)+22.5)/45.0)])
   

###############################################################################
# OpenWeatherMap_Data #########################################################
class OpenWeatherMap_Data (threading.Thread):
    """reads weather data from openweathermap and provides it to
       the sensorvaluequeue and as a property (OpenWeatherMap_Data.weather)
    """

    OWMC = OpenWeatherMap_Config

    def __init__ (self, sv_queue):
        """sv_queue: method to be called for sending all weather 
           data to my SensorValueQueue"""
        threading.Thread.__init__(self)
        self.sv_queue = sv_queue
        self.__lock = threading.Lock()
        self.__weather = []
        self.read_data()
        self.send_sensor_values()

        self.__running = True

    def get_forecast (self):
        """reads forecast weather data from openweathermap"""
        try:
            with urlopen(self.OWMC.url_forecast) as response:
                data = json.loads(response.read().decode("utf-8"))
        except HTTPError:
            raise ValueError

        # get data from 12:00 am only
        forecast_owm = [ data['list'][i] 
                         for i in range(len(data['list'])) 
                         if "12:00:00" in data['list'][i]['dt_txt'] ]

        forecast = []
        for i in range(len(forecast_owm)):
            try:  # if wind speed is almost 0, no direction is set
                forecast_owm[i]['wind']['deg']
            except KeyError:
                forecast_owm[i]['wind']['deg'] = None

            forecast.append({
                 'temp': "{:.1f}".format(forecast_owm[i]['main']['temp']),
                 'humidity': "{:.1f}".format(forecast_owm[i]['main']['humidity']),
                 'wind': "{:.1f}".format(forecast_owm[i]['wind']['speed']),
                 'wind direction': self.OWMC.direction(forecast_owm[i]['wind']['deg']),
                 'desc': forecast_owm[i]['weather'][0]['description'],
                 'icon_url': self.OWMC.icon_url(forecast_owm[i]['weather'][0]['icon']),
                 'time': forecast_owm[i]['dt'],
                 'time_text': forecast_owm[i]['dt_txt']
                })
        return forecast

    def get_actual (self):
        """reads current weather data from openweathermap"""
        try:
            with urlopen(self.OWMC.url_actual) as response:
                data = json.loads(response.read().decode("utf-8"))
        except HTTPError:
            raise ValueError

        try:  # if wind speed is almost 0, no direction is set
            data['wind']['deg']
        except KeyError:
            data['wind']['deg'] = None

        return {'temp': "{:.1f}".format(data['main']['temp']),
                'humidity': "{:.1f}".format(data['main']['humidity']),
                'wind': "{:.1f}".format(data['wind']['speed']),
                'wind direction': self.OWMC.direction(data['wind']['deg']),
                'desc': data['weather'][0]['description'],
                'icon_url': self.OWMC.icon_url(data['weather'][0]['icon']),
                'time': data['dt'],
                'time_text': datetime.fromtimestamp(data['dt']).isoformat(' ')
               }

    def read_data (self):
        try:
            w = [ self.get_actual() ] + self.get_forecast()
        except ValueError:
            pass
        else:  # update only if there was no error when reading data from owm.
            with self.__lock: 
                self.__weather = w

    def send_sensor_values (self):
        self.sv_queue(self.weather)

    @property
    def weather (self):
        with self.__lock:
            return copy.deepcopy(self.__weather)

    def run (self):
        i = 0
        while self.__running:
            time.sleep(0.1)
            i += 1
            if i > 1200:
                self.read_data()
                self.send_sensor_values()
                i = 0

    def stop (self):
        self.__running = False


###############################################################################
# OWM_Sensorvalues ############################################################
class OWM_Sensorvalues (object):
    number_of_datasets = 3

    def __init__ (self):
        self.qv = []
        for i in range(self.number_of_datasets):
            self.qv.append({'temp': SensorValueLock("ID_OWM_{}1".format(i), "TempOWM_{}".format(i), SensorValue.Types.Temp, "°C", threading.Lock()),
                            'humidity': SensorValueLock("ID_OWM_{}2".format(i), "HumiOWM_{}".format(i), SensorValue.Types.Humi, "% rF", threading.Lock()),
                            'wind': SensorValueLock("ID_OWM_{}3".format(i), "WindOWM_{}".format(i), SensorValue.Types.Wind, "km/h", threading.Lock()),
                            'wind direction': SensorValueLock("ID_OWM_{}4".format(i), "WindDirOWM_{}".format(i), SensorValue.Types.WindDir, None, threading.Lock()),
                            'desc': SensorValueLock("ID_OWM_{}5".format(i), "DescOWM_{}".format(i), SensorValue.Types.Desc, None, threading.Lock()),
                            'icon_url': SensorValueLock("ID_OWM_{}6".format(i), "IconOWM_{}".format(i), SensorValue.Types.IconUrl, None, threading.Lock())
                           })
            for k, qv in self.qv[i].items():
                sq.register(qv)

    def senddatatoqueue (self, data):
        print("=== {} ===================".format(datetime.now()))
        for i in range(self.number_of_datasets):
            for k, qv in self.qv[i].items():
                print("i: {}; {}: {}".format(i, k, data[i][k]))
                qv.value = str(data[i][k])


###############################################################################
# Shutdown ####################################################################
class Shutdown (object):
    terminate = False

    def __init__ (self, shutdown_func=None):
        self.shutdown_func = shutdown_func
        signal.signal(signal.SIGTERM, self.shutdown)
        signal.signal(signal.SIGINT, self.shutdown)

    def shutdown (self, __s, __f):
        self.terminate = True
        if self.shutdown_func:
             self.shutdown_func()


def shutdown_application ():
    owm_data.stop()
    owm_data.join()
    sq.stop()
    sq.join()
    sys.exit(0)


###############################################################################
# Main ########################################################################
if __name__ == '__main__':
    shutdown = Shutdown(shutdown_func=shutdown_application)

    sq = SensorQueueClient_write()
    owm_sv = OWM_Sensorvalues()
    sq.start()

    owm_data = OpenWeatherMap_Data(owm_sv.senddatatoqueue)
    owm_data.start()

    app.run(host="0.0.0.0")

# eof #

