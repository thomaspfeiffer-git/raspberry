# -*- coding: utf-8 -*-
##############################################################################
# SHT31.py                                                                   #
# TODO
# (c) https://github.com/thomaspfeiffer-git 2019                             #
##############################################################################
"""
TODO   
"""

import time

from i2c import I2C
from Logging import Log


SHT31_BASEADDR = 0x44
SHT31_SECONDARYADDR = 0x45


class SHT31 (I2C):
    def __init__ (self, addr=SHT31_BASEADDR, lock=None):
        I2C.__init__(self, lock)
        self.i2c_addr = addr

        self.__temperature = 0
        self.__humidity = 0
        self.__lastread = -1

    def __read (self):
        if self.__lastread+30 < time.time(): # wait at least 30 seconds until 
            self.__lastread = time.time()    # until next update
            with I2C._lock:
                I2C._bus.write_i2c_block_data(self.i2c_addr, 0x2C, [0x06])
                time.sleep(0.5)
                data = I2C._bus.read_i2c_block_data(self.i2c_addr, 0x00, 6)

            temp = data[0] * 256 + data[1]
            self.__temperature = -45 + (175 * temp / 65535.0)
            self.__humidity = 100 * (data[3] * 256 + data[4]) / 65535.0

    def read_temperature (self):
        self.__read()
        return self.__temperature


    def read_humidity (self):
        self.__read()
        return self.__humidity

# eof #

