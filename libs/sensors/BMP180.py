# -*- coding: utf-8 -*-
###############################################################################
# BMP180.py                                                                   #
# Communication with BMP180                                                   #
# (c) https://github.com/thomaspfeiffer-git 2016, 2023                        #
###############################################################################
"""provides a class for handling the air pressure sensor BMP180"""

from time import localtime
import sys

from sensors.Adafruit import Adafruit_BMP085
from i2c import I2C


class BMP180 (I2C):
    """class for handling the air pressure sensor BMP085"""
    def __init__ (self, lock=None):
        if sys.version_info >= (3,0):
            super().__init__(lock)
        else:
            super(BMP180, self).__init__(lock)

        self.__bmp    = Adafruit_BMP085.BMP085(mode=Adafruit_BMP085.BMP085_ULTRAHIGHRES)

    def read_pressure (self):
        """read pressure and return measured value"""
        with I2C._lock:
            try:
                return self.__bmp.read_pressure()
            except (IOError, OSError):
                print(localtime()[3:6], "error reading/writing i2c bus in BMP180.read_pressue()")

        return None

    def read_temperature (self):
        """read temperature and return measured value"""
        with I2C._lock:
            try:
                return self.__bmp.read_temperature()
            except (IOError, OSError):
                print(localtime()[3:6], "error reading/writing i2c bus in BMP180.read_temperature()")

        return None

# eof #

