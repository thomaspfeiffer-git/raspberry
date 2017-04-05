#!/usr/bin/python3
# -*- coding: utf-8 -*-
##############################################################################
# Brightness.py                                                              #
# (c) https://github.com/thomaspfeiffer-git 2017                             #
##############################################################################
"""controls brightness of a raspberry pi display based on the
   luminosity measured by a TSL2561"""

### usage ###
# TODO 


from datetime import datetime
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
from Shutdown import Shutdown


CONTROLBRIGHTNESS = '/sys/class/backlight/rpi_backlight/brightness'


##############################################################################
# Sensor #####################################################################
class Sensor (threading.Thread):
    """todo """

    MIN = 15
    MAX = 255

    def __init__ (self):
        threading.Thread.__init__(self)
        self.sensor    = TSL2561()
        self.__lux     = 0
        self.__running = False

    @property
    def lux (self):
        return self.__lux

    def run (self):
        self.__running = True
        while self.__running:
            v = self.sensor.lux() * 2
            if v < self.MIN: v = self.MIN
            if v > self.MAX: v = self.MAX
            self.__lux = v
            time.sleep(1)

    def stop (self):
        self.__running = False


##############################################################################
# Control ####################################################################
class Control (threading.Thread):
    """todo """

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

                # print("command:", command)
                subprocess.call(command, shell=True)

        return set_value

    def switch_on (self):
        self.__switchedon = True
        self.timestamp = datetime.timestamp(seconds=DELAYTOLIGHTOFF)

    def switched_on (self):
        if datetime.now() > self.timestamp:
            self.__switchedon = False
        return self.__switchedon

    def run (self):
        self.__running = True
        measurements = Measurements(maxlen=20)
        set_brightness = self.set_brightness()

        while self.__running:
            measurements.append(sensor.lux)
                    # full brightness between 6 am and 10 pm or
                    # if manually switched on
            if 6 <= datetime.now().hour < 18 or self.switched_on(): 
                set_brightness(Sensor.MAX)   
            else:
                set_brightness(int(measurements.avg()))
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

    while True:
        time.sleep(0.1)

# eof #

