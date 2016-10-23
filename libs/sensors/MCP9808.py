# -*- coding: utf-8 -*-
################################################################################
# MCP9808.py                                                                   #
# (c) https://github.com/thomaspfeiffer-git 2016                               #
################################################################################
"""control temperature sensor MCP9808."""

# Source code taken and modified from:
# * https://github.com/adafruit/Adafruit_Python_MCP9808/blob/master/Adafruit_MCP9808/MCP9808.py
# * https://github.com/mercolino/MCP9808/blob/master/MCP9808/mcp9808.py

import sys
from time import localtime

from i2c import I2C


MCP9808_ADDR           = 0x18

MCP9808_REG_TEMP       = 0x05
MCP9808_REG_RESOLUTION = 0x08



class MCP9808 (I2C):
    def __init__ (self, qvalue=None, lock=None):
        if sys.version_info >= (3,0):
            super().__init__(lock)
        else:
            super(MCP9808, self).__init__(lock)

        self._address    = MCP9808_ADDR
        self.__qvalue    = qvalue
        self.__lastvalue = 0

        self.set_resolution(0x03) # Set resolution to 0.0625. #


    def read_temperature (self):
        with I2C._lock:
            try:
                t = I2C._bus.read_word_data(self._address, MCP9808_REG_TEMP)

                # Scale and convert to signed value.
                upperByte = t & 0x0F00
                lowerByte = t & 0x00FF
                if t & 0x1000:
                    temp = (((upperByte >> 8) * 16) + (lowerByte / 16.0)) * (-1)
                else:
                    temp = ((upperByte >> 8) * 16) + (lowerByte / 16.0)

                self.__lastvalue = temp

            except (IOError, OSError):
                print(localtime()[3:6], "error reading/writing i2c bus")

            finally:
                if self.__qvalue is not None:
                    value = "%.1f" % (self.__lastvalue)
                    self.__qvalue.value = value

                return self.__lastvalue


    def set_resolution (self, resolution):
        with I2C._lock:
            try:
                I2C._bus.write_byte_data(self._address, MCP9808_REG_RESOLUTION, resolution)

            except (IOError, OSError):
                print(localtime()[3:6], "error reading/writing i2c bus")

# eof #

