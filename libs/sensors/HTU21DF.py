# -*- coding: utf-8 -*-
################################################################################
# HTU21DF.py                                                                   #
# (c) https://github.com/thomaspfeiffer-git 2016                               #
################################################################################
"""control temperature and humidity sensor HTU21DF (also known as Si7021)"""

# Source code taken and modified from:
# https://github.com/dalexgray/RaspberryPI_HTU21DF/blob/master/HTU21DF.py
# https://github.com/raspberrypi/weather-station/blob/master/HTU21D.py

import array
import sys
from time import strftime, sleep

from i2c import I2C


HTU21DF_BASE_ADDR = 0x40

# HTU21D-F Commands
HTU21DF_READTEMP = 0xE3
HTU21DF_READHUMI = 0xE5
wtreg = 0xE6
rdreg = 0xE7
HTU21DF_RESET    = 0xFE


class HTU21DF (I2C):
    def __init__ (self, address=HTU21DF_BASE_ADDR,  qvalue_temp=None, qvalue_humi=None, lock=None):
        if sys.version_info >= (3,0):
            super().__init__(lock)
        else:
            super(HTU21DF, self).__init__(lock)

        self._address     = address
        self.__qvalue_temp     = qvalue_temp    
        self.__qvalue_humidity = qvalue_humi    
        self.__lastvalues = {'temperature': 0,
                             'humidity': 0}
        self.reset()


    def reset (self):
        with I2C._lock:
            I2C._bus.write_byte(self._address, HTU21DF_RESET)
        sleep(0.1)


    def _read (self, register):
        with I2C._lock:
            I2C._bus.write_byte(self._address, register)
            sleep(0.055)
            I2C._bus._select_device(self._address)
            data = I2C._bus._device.read(3)
        return data


    def read_temperature (self):
        try:
            buf = array.array('B', self._read(HTU21DF_READTEMP))
            t = (buf[0] * 256.0) + buf[1]
            t = ((t / 65536.0) * 175.72 ) - 46.85
            self.__lastvalues['temperature'] = t
            if self.__qvalue_temp is not None:
                self.__qvalue_temp.value = "%.1f" % (t)

        except (IOError, OSError):
            print(strftime("%Y%m%d %X:"), "error reading/writing i2c bus in HTU21DF.read_temperature()")

        finally:
            return self.__lastvalues['temperature']


    def read_humidity (self):
        t = self.read_temperature()

        try:
            buf = array.array('B', self._read(HTU21DF_READHUMI))
            h = (buf[0] * 256.0) + buf[1]
            h = ((h / 65536.0) * 125 ) - 6 
            h = h + (25 - t) * -0.15
            self.__lastvalues['humidity'] = h
            if self.__qvalue_humidity is not None:
                self.__qvalue_humidity.value = "%.1f" % (h)

        except (IOError, OSError):
            print(strftime("%Y%m%d %X:"), "error reading/writing i2c bus in HTU21DF.read_humidity()")

        finally:
            return self.__lastvalues['humidity']

# eof #

