# -*- coding: utf-8 -*-
###############################################################################
# BME280.py                                                                   #
# Communication with BME280                                                   #
# (c) https://github.com/thomaspfeiffer-git 2016, 2023                        #
###############################################################################
"""provides a class for handling sensor BME280"""

from time import strftime
import sys

from sensors.Adafruit import Adafruit_BME280
from i2c import I2C


class BME280 (I2C):
    """class for handling the air pressure sensor BME280"""
    def __init__ (self, lock=None):
        if sys.version_info >= (3,0):
            super().__init__(lock)
        else:
            super(BME280, self).__init__(lock)

        self.__bme             = Adafruit_BME280.BME280()
        self.__lastvalues      = {'pressure': 0,
                                  'temperature': 0,
                                  'humidity': 0}


    def read_pressure (self):
        """read pressure and return measured value"""
        with I2C._lock:
            try:
                value = self.__bme.read_pressure()
                self.__lastvalues['pressure'] = value

            except (IOError, OSError):
                print(strftime("%Y%m%d %X:"), "error reading/writing i2c bus in BME280.read_pressue()")

            finally:
                return self.__lastvalues['pressure']

        return None


    def read_temperature (self):
        """read temperature and return measured value"""
        with I2C._lock:
            try:
                value = self.__bme.read_temperature()
                self.__lastvalues['temperature'] = value

            except (IOError, OSError):
                print(strftime("%Y%m%d %X:"), "error reading/writing i2c bus in BME280.read_temperature()")

            finally:
                return self.__lastvalues['temperature']

        return None


    def read_humidity (self):
        """read humidity and return measured value"""
        with I2C._lock:
            try:
                value = self.__bme.read_humidity()
                self.__lastvalues['humidity'] = value

            except (IOError, OSError):
                print(strftime("%Y%m%d %X:"), "error reading/writing i2c bus in BME280.read_humidity()")

            finally:
                return self.__lastvalues['humidity']

        return None

# eof #

