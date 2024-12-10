#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
##############################################################################
# Brightness.py                                                              #
# (c) https://github.com/thomaspfeiffer-git 2017, 2024                       #
##############################################################################
"""controls brightness of a raspberry pi display based on the
   luminosity measured by a TSL2561 in prozess Sensors/Sensors.py"""

### usage ###
# run programm: nohup ./Brightness.py &
# call in case of a touch event: http://<host>:5000/touchevent


### setup ###
# sudo pip3 install flask-restful
# sudo pip3 install --break-system-packages attridict


import attridict
from datetime import datetime, timedelta
import json
import socket
import subprocess
import sys
import threading
import time
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

sys.path.append('../../libs')
sys.path.append('../../libs/sensors')  # TODO beautify import paths
sys.path.append('../../libs/sensors/Adafruit')

from Logging import Log
from Measurements import Measurements
from Shutdown import Shutdown


from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


###############################################################################
# CONFIG ######################################################################
class CONFIG (object):
    URL_API_LIGHTNESS = "http://pih2:5001"
    CONTROLBRIGHTNESS = '/sys/class/backlight/10-0045/brightness'
    # if necessary:
    #   config = configparser.ConfigParser()
    #   config.read(configfilename)


###############################################################################
# APIs ########################################################################
class API_Touchevent (Resource):
    def get (self):
        if control.schedule_on() or control.switched_on() or control.prettybright():
            result = { 'FullBrightness': True }
        else:
            result = { 'FullBrightness': False }

        control.switch_on()
        return result

class API_Brightness (Resource):
    def get (self):
         return sensor.lux

api.add_resource(API_Touchevent, '/touchevent')
api.add_resource(API_Brightness, '/brightness')


##############################################################################
# Sensor #####################################################################
class Sensor (threading.Thread):
    """todo """

    MIN = 15
    MAX = 255

    def __init__ (self):
        threading.Thread.__init__(self)
        self.url = CONFIG.URL_API_LIGHTNESS
        self.__lux_calced = 0
        self.__lux        = 0
        self.__running = False

    def _read_sensor (self):
        lightness = self.__lux
        try:
            with urlopen(self.url, timeout=15) as response:
                lightness = int(attridict(json.loads(response.read().decode("utf-8")))['lightness'])
        except (HTTPError, URLError):
            Log("HTTPError, URLError: {0[0]} {0[1]}".format(sys.exc_info()))
        except socket.timeout:
            Log("socket.timeout: {0[0]} {0[1]}".format(sys.exc_info()))
        except ConnectionResetError:
            Log("ConnectionResetError: {0[0]} {0[1]}".format(sys.exc_info()))
        except ConnectionRefusedError:
            Log("ConnectionRefusedError: {0[0]} {0[1]}".format(sys.exc_info()))
        finally:
            return lightness

    @property
    def lux_calced (self):
        return self.__lux_calced

    @property
    def lux (self):
        return self.__lux

    def run (self):
        self.__running = True
        while self.__running:
            v = self._read_sensor()
            self.__lux = v
            v = v * 2
            if v < self.MIN: v = self.MIN
            if v > self.MAX: v = self.MAX
            self.__lux_calced = v
            time.sleep(1)

    def stop (self):
        self.__running = False


##############################################################################
# Control ####################################################################
class Control (threading.Thread):
    """controls brightness of display"""

    DELAYTOLIGHTOFF = 15

    def __init__ (self):
        threading.Thread.__init__(self)
        self.timestamp  = datetime.now()
        self.__switchedon = False
        self.__running = False

    @staticmethod
    def set_brightness ():
        lastvalue = 0

        def set_value (brightness):
            nonlocal lastvalue

            if brightness != lastvalue:
                lastvalue = brightness

                command = "sudo bash -c \"echo \\\"{}\\\" > {}\""
                command = command.format(brightness, CONFIG.CONTROLBRIGHTNESS)
                subprocess.call(command, shell=True)

        return set_value

    def switch_on (self):
        self.__switchedon = True
        self.timestamp = datetime.now() + timedelta(seconds=self.DELAYTOLIGHTOFF)

    def switched_on (self):
        if datetime.now() > self.timestamp:
            self.__switchedon = False
        return self.__switchedon

    def prettybright (self):
        """no need to set display to full brightness
           if it is already very bright"""
        return self.measurements.avg() > Sensor.MAX - 5

    @staticmethod
    def schedule_on ():
        """full brightness from 6 am to 10 pm"""
        return 6 <= datetime.now().hour < 22

    def run (self):
        self.__running = True
        self.measurements = Measurements(maxlen=20)
        set_brightness = self.set_brightness()

        while self.__running:
            self.measurements.append(sensor.lux_calced)
                    # full brightness between 6 am and 10 pm or
                    # if manually switched on
            if self.schedule_on() or self.switched_on():
                set_brightness(Sensor.MAX)
            else:
                set_brightness(int(self.measurements.avg()))
            time.sleep(0.02)

        set_brightness(Sensor.MAX) # set max brightness on exit

    def stop (self):
        self.__running = False


###############################################################################
# shutdown_application ########################################################
def shutdown_application ():
    """called on shutdown; stops all threads"""
    print("in shutdown_application()")
    control.stop()
    control.join()
    sensor.stop()
    sensor.join()
    sys.exit(0)


###############################################################################
# Main ########################################################################
if __name__ == '__main__':
    shutdown = Shutdown(shutdown_func=shutdown_application)

    sensor = Sensor()
    sensor.start()

    control = Control()
    control.start()

    app.run(host="0.0.0.0")

# eof #

