# -*- coding: utf-8 -*-
################################################################################
# PCF8591.py                                                                   #
# (c) https://github.com/thomaspfeiffer-git 2016                               #
################################################################################
"""controls A/D converter PCF8591"""

from i2c import I2C
from time import localtime

class PCF8591 (I2C):
    def __init__ (self, address, lock=None):
        super().__init__(lock)
        self._address    = address
        self.__lastvalue = 0

    def read (self, channel=0):
        with I2C._lock:
            try:
                I2C._bus.write_byte(self._address, 0x40|channel)
                _ = I2C._bus.read_byte(self._address) # seems to be a quite useless acknowledge
                res = I2C._bus.read_byte(self._address) 
                self.__lastvalue = res

            except (IOError, OSError):
                print(localtime()[3:6], "error reading/writing i2c bus")

            finally:
                return self.__lastvalue


    def write (self, value):
        raise NotImplementedError

# eof #

