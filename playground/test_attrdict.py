#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2017                   #
###############################################################################

### usage ###
# nohup ./openweather.py > openweather.log 2>openweather.err &


### setup ###
# sudo pip3 install attrdict

from attrdict import AttrDict
import copy
from datetime import datetime
import json
from os.path import expanduser
import pprint
import sys
import time
from urllib.error import HTTPError
from urllib.request import urlopen


###############################################################################
# OpenWeatherMap_Config #######################################################
class OpenWeatherMap_Config (object):
    """provides some configuration and static methods for the
       api call to openweathermap
    """
    def read_api_key ():
        with open(expanduser('~') + "/keys/openweathermap.key", "r") as key_file:
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
class OpenWeatherMap_Data (object):
    """reads weather data from openweathermap and provides it to
       the sensorvaluequeue and as a property (OpenWeatherMap_Data.weather)
    """

    OWMC = OpenWeatherMap_Config

    def __init__ (self):
        """sv_queue: method to be called for sending all weather 
           data to my SensorValueQueue
        """
        self.__weather = []

    def convert (self, data):
        try:       # if wind speed is almost 0, no direction is set
            _ = data.wind.deg
        except AttributeError:
            data.wind.deg = None

        return {'temp': "{:.1f}".format(data.main.temp),
                 'humidity': "{:.1f}".format(data.main.humidity),
                 'wind': "{:.1f}".format(data.wind.speed),
                 'wind direction': self.OWMC.direction(data.wind.deg),
                 'desc': data.weather[0].description,
                 'icon_url': self.OWMC.icon_url(data.weather[0].icon),
                 'time': data.dt,
                 'time_text': datetime.fromtimestamp(data.dt).isoformat(' ')
                }

    def get_forecast (self):
        """reads forecast weather data from openweathermap"""
        try:
            with urlopen(self.OWMC.url_forecast) as response:
                data = AttrDict(json.loads(response.read().decode("utf-8")))
        except HTTPError:
            raise ValueError

        # get data from 12:00 am only
        forecast = [ data.list[i] 
                     for i in range(len(data.list)) 
                     if "12:00:00" in data.list[i].dt_txt ]

        return [ self.convert(forecast[i]) for i in range(len(forecast)) ]

    def get_actual (self):
        """reads current weather data from openweathermap"""
        try:
            with urlopen(self.OWMC.url_actual) as response:
                data = AttrDict(json.loads(response.read().decode("utf-8")))
        except HTTPError:
            raise ValueError

        return self.convert(data)

    def read_data (self):
        """reads actual weather data and forecast and stores
           these data in self.__weather
        """
        try:
            w = [ self.get_actual() ] + self.get_forecast()
        except ValueError:
            pass
        else:  # update only if there was no error when reading data from owm.
            self.__weather = w

    @property
    def weather (self):
        return copy.deepcopy(self.__weather)


###############################################################################
# Main ########################################################################
if __name__ == '__main__':

    owm_data = OpenWeatherMap_Data()

    while True:
        owm_data.read_data()
        pprint.pprint(owm_data.weather)
        time.sleep(120)

# eof #

