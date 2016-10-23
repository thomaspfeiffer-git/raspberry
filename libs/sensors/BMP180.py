# -*- coding: utf-8 -*-
###############################################################################
# BMP180.py                                                                   #
# Communication with BMP180                                                   #
# (c) https://github.com/thomaspfeiffer-git 2016                              #
###############################################################################
"""provides a class for handling the air pressure sensor BMP085"""

import sys

from Adafruit import Adafruit_BMP085
from i2c import I2C



class BMP180 (I2C):
    """class for handling the air pressure sensor BMP085"""
    def __init__ (self, qvalue=None, lock=None):
        if sys.version_info >= (3,0):
            super().__init__(lock)
        else:
            super(BMP180, self).__init__(lock)

        self.__bmp    = Adafruit_BMP085.BMP085(mode=Adafruit_BMP085.BMP085_ULTRAHIGHRES) 
        self.__qvalue = qvalue


    def read_pressure (self):
        """read pressure and return measured value"""
        value = -1
        with I2C._lock:
            try:
                value = self.__bmp.read_pressure()

            except (IOError, OSError):
                print(localtime()[3:6], "error reading/writing i2c bus in read_pressue()")

            finally:
                if self.__qvalue is not None:
                    self.__qvalue.value = "%.1f" % (value/100.0)

                return value


    def read_temperature (self):
        """read temperature and return measured value"""
        value = -1
        with I2C._lock:
            try:
                value = self.__bmp.read_temperature()
    
            except (IOError, OSError):
                print(localtime()[3:6], "error reading/writing i2c bus in read_temperature()")

            finally:
                return value

# eof #

