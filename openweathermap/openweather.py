#!/usr/bin/python3 -u

# weather icons:
# https://openweathermap.org/weather-conditions

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

# provide api:
# http://flask-restful.readthedocs.io/en/latest/quickstart.html#a-minimal-api

# install
# sudo pip3 install flask-restful

"""
from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class API_OpenWeatherData (Resource):
    def get (self):
        return json.dumps(forecast)

api.add_resource(API_OpenWeatherData, '/')
"""

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

    @classmethod
    def direction (cls, degrees):
        degrees = int(degrees)
        if 22.5 <= degrees < 22.5+45:
            return "nord-ost"
        if 67.5 <= degrees < 67.5+45:
            return "ost"
        if 112.5 <= degrees < 112.5+45:
            return "süd-ost"
        if 157.5 <= degrees < 157.5+45:
            return "süd"
        if 202.5 <= degrees < 202.5+45:
            return "süd-west"
        if 247.5 <= degrees < 247.5+45:
            return "west"
        if 292.5 <= degrees < 292.5+45:
            return "nord-west"
        if 337.5 <= degrees <= 360 or 0 <= degrees < 22.5:
            return "nord" 
    
    """TODO: prevent from instantiating"""


class OpenWeatherMap_Data (threading.Thread):
    """ todo """
    def __init__ (self, sv_queue):
        """todo: describe sv_queue"""
        threading.Thread.__init__(self)
        self.sv_queue = sv_queue
        self.__lock = threading.Lock()
        self.__weather = []
        self.read_data()
        self.send_sensor_values()

        self.__running = True

    def __str__ (self):
        pass

    def get_forecast (self):
        try:
            with urlopen(OpenWeatherMap_Config.url_forecast) as response:
                data = json.loads(response.read().decode("utf-8"))
        except HTTPError:
            raise ValueError

        # get data from 12:00 am only
        forecast_owm = [ data['list'][i] 
                         for i in range(len(data['list'])) 
                         if "12:00:00" in data['list'][i]['dt_txt'] ]

        forecast = []
        for i in range(len(forecast_owm)):
            forecast.append({
                 'temp': "{:.1f}".format(forecast_owm[i]['main']['temp']),
                 'humidity': "{:.1f}".format(forecast_owm[i]['main']['humidity']),
                 'wind': "{:.1f}".format(forecast_owm[i]['wind']['speed']),
                 'wind direction': OpenWeatherMap_Config.direction(forecast_owm[i]['wind']['deg']),
                 'desc': forecast_owm[i]['weather'][0]['description'],
                 'icon_url': OpenWeatherMap_Config.icon_url(forecast_owm[i]['weather'][0]['icon']),
                 'time': forecast_owm[i]['dt'],
                 'time_text': forecast_owm[i]['dt_txt']
                })
        return forecast

    def get_actual (self):
        try:
            with urlopen(OpenWeatherMap_Config.url_actual) as response:
                data = json.loads(response.read().decode("utf-8"))
        except HTTPError:
            raise ValueError

        return {'temp': "{:.1f}".format(data['main']['temp']),
                'humidity': "{:.1f}".format(data['main']['humidity']),
                'wind': "{:.1f}".format(data['wind']['speed']),
                'wind direction': OpenWeatherMap_Config.direction(data['wind']['deg']),
                'desc': data['weather'][0]['description'],
                'icon_url': OpenWeatherMap_Config.icon_url(data['weather'][0]['icon']),
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
        print("=====================================")
        for i in range(self.number_of_datasets):
            for k, qv in self.qv[i].items():
                print("i: {}; {}: {}".format(i, k, data[i][k]))
                qv.value = str(data[i][k])


###############################################################################
# Exit ########################################################################
def _exit():
    """cleanup stuff"""
    oo.stop()
    oo.join()
    sq.stop()
    sq.join()
    sys.exit()

def __exit(__s, __f):
    """cleanup stuff used for signal handler"""
    _exit()


###############################################################################
# Main ########################################################################
signal.signal(signal.SIGTERM, __exit)
signal.signal(signal.SIGINT, __exit)

sq = SensorQueueClient_write()
owm_sv = OWM_Sensorvalues()
sq.start()

oo = OpenWeatherMap_Data(owm_sv.senddatatoqueue)
oo.start()

"""
if __name__ == '__main__':
    app.run()
"""

# eof #

