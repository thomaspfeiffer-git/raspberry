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


##############################################################################
# Control ####################################################################
class Control (threading.Thread):
    MIN = 15
    MAX = 255
    sensor = TSL2561()

    def __init__ (self):
        threading.Thread.__init__(self)
        self.__running = False

    def run (self):
        self.__running = True
        measurements = Measurements(maxlen=20)

        while self.__running:
            lux = int(sensor.lux()) * 2
            if lux < self.MIN: lux = self.MIN
            if lux > self.MAX: lux = self.MAX
            measurements.append(lux)
            avg = int(measurements.avg())

            # TODO: call only on change of value etc
            command = "sudo bash -c \"echo \\\"{}\\\" > /sys/class/backlight/rpi_backlight/brightness\"".format(avg)

            # print("command:", command)
            subprocess.call(command, shell=True)

            time.sleep(0.1)

    def stop (self):
        # TODO set brightness to self.MAX on exit
        self.__running = False


###############################################################################
# shutdown_application ########################################################
def shutdown_application ():
    """called on shutdown; stops all threads"""
    print("in shutdown_application()")
    control.stop()
    control.join()
    sys.exit(0)


###############################################################################
# Main ########################################################################
if __name__ == '__main__':
    shutdown = Shutdown(shutdown_func=shutdown_application)
    control = Control()
    control.start()

    while True:
        time.sleep(0.1)

# eof #

