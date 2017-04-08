#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
##############################################################################
# Brightness.py                                                              #
# (c) https://github.com/thomaspfeiffer-git 2017                             #
##############################################################################
"""controls brightness of a raspberry pi display based on the
   luminosity measured by a TSL2561"""

### usage ###
# run programm: nohup ./Brightness.py &
# call in case of a touch event: http://<host>:5000/touchevent


### setup ###
# sudo pip3 install flask-restful


from datetime import datetime, timedelta
import subprocess
import sys
import threading
import time

sys.path.append('../../libs')
sys.path.append('../../libs/sensors')  # TODO beautify import paths
sys.path.append('../../libs/sensors/Adafruit')

from i2c import I2C
from Measurements import Measurements
from sensors.TSL2561 import TSL2561
from SensorQueue2 import SensorQueueClient_write
from SensorValue2 import SensorValue, SensorValue_Data
from Shutdown import Shutdown


from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


CONTROLBRIGHTNESS = '/sys/class/backlight/rpi_backlight/brightness'


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

    def __init__ (self, qvalue=None):
        threading.Thread.__init__(self)
        self.sensor       = TSL2561()
        self.__qvalue     = qvalue
        self.__lux_calced = 0
        self.__lux        = 0
        self.__running = False

    @property
    def lux_calced (self):
        return self.__lux_calced

    @property
    def lux (self):
        return self.__lux

    def run (self):
        self.__running = True
        while self.__running:
            v = self.sensor.lux()
            if self.__qvalue is not None:
                self.__qvalue = str(v)

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
                command = command.format(brightness, CONTROLBRIGHTNESS)
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
    qv_brightness = SensorValue("ID_09", "LightKitchen", SensorValue_Data.Types.Light, "lux")
    sq = SensorQueueClient_write("../config.ini")
    sq.register(qv_brightness)

    sensor = Sensor(qvalue=qv_brightness)
    sensor.start()

    control = Control()
    control.start()

    app.run(host="0.0.0.0")

# eof #

