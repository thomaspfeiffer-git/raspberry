#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# Sensors.py                                                                  #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2019                   #
###############################################################################

"""
TODO
"""

import sys
import threading
import time


sys.path.append("../libs/")

from Logging import Log

from sensors.CPU import CPU
from sensors.DS1820 import DS1820
from sensors.HTU21DF import HTU21DF
from sensors.PCF8591 import PCF8591
from sensors.SHT31 import SHT31, SHT31_BASEADDR, SHT31_SECONDARYADDR


class Sensors (threading.Thread):
    def __init__ (self):
        threading.Thread.__init__(self)

        self.cpu = CPU()
        # self.ds1820_outdoor = DS1820()
        # self.ds1820_water = DS1820()
        self.htu21_box = HTU21DF()
        self.sht31_airin = SHT31(addr=SHT31_BASEADDR)
        self.sht31_airout = SHT31(addr=SHT31_SECONDARYADDR)
        self.pcf8591 = PCF8591()

        self.__data = dict()
        self._running = True

    @property
    def data (self):
        return self.__data

    # def run (self):
    #    while self._running:
    def read_once (self):
        if True:
            self.__data.update(cpu = self.cpu.read_temperature())
            self.__data.update(box_temp = self.htu21_box.read_temperature())
            self.__data.update(box_humidity = self.htu21_box.read_humidity())
            self.__data.update(airin_temp = self.sht31_airin.read_temperature())
            self.__data.update(airin_humidity = self.sht31_airin.read_humidity())
            self.__data.update(airout_temp = self.sht31_airout.read_temperature())
            self.__data.update(airout_humidity = self.sht31_airout.read_humidity())
            self.__data.update(engines_circulation = self.pcf8591.read(channel=0))
            self.__data.update(engines_countercurrent = self.pcf8591.read(channel=1))
            print(self.__data)

    def stop (self):
        self._running = False

# eof #

