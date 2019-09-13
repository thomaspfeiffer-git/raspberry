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


class Sensordata (object):
    def __init__ (self):
        self.valid = False
        self.cpu = None
        self.box_temp = None
        self.box_humidity = None
        self.airin_temp = None
        self.airin_humidity = None
        self.airout_temp = None
        self.airout_humidity = None
        self.engines_circulation = None
        self.engines_countercurrent = None
        self.outdoor_temp = None
        self.water_temp = None

    def __str__ (self):
        if self.valid:
            print "test cpu: {0.cpu:.2f}".format(self)
            return "CPU:      {cpu:.2f} °C\n" \
                   "Temp Box: {:.2f} °C\n" \
                   "Humi Box: {:.2f} % rF\n" \
                   "Temp Air in: {:.2f} °C\n" \
                   "Humi Air in: {:.2f} % rF\n"  \
                   "Temp Air out: {:.2f} °C\n" \
                   "Humi Air out: {:.2f} % rF\n" \
                   .format(self.cpu, self.box_temp, self.box_humidity,
                           self.airin_temp, self.airin_humidity,
                           self.airout_temp, self.airout_humidity)
        else:
            return "Sensordata not valid."


class Sensors (threading.Thread):
    def __init__ (self, data):
        threading.Thread.__init__(self)

        self.cpu = CPU()
        self.ds1820_outdoor = DS1820("/sys/bus/w1/devices/28-000008561957/w1_slave")
        # self.ds1820_water = DS1820()
        self.htu21_box = HTU21DF()
        self.sht31_airin = SHT31(addr=SHT31_BASEADDR)
        self.sht31_airout = SHT31(addr=SHT31_SECONDARYADDR)
        self.pcf8591 = PCF8591()

        self.__data = data
        self._running = True

    # def run (self):
    #    while self._running:
    def read_once (self):
        if True:
            self.__data.cpu = self.cpu.read_temperature()
            self.__data.box_temp = self.htu21_box.read_temperature()
            self.__data.box_humidity = self.htu21_box.read_humidity()
            self.__data.airin_temp = self.sht31_airin.read_temperature()
            self.__data.airin_humidity = self.sht31_airin.read_humidity()
            self.__data.airout_temp = self.sht31_airout.read_temperature()
            self.__data.airout_humidity = self.sht31_airout.read_humidity()
            self.__data.engines_circulation = self.pcf8591.read(channel=0)
            self.__data.engines_countercurrent = self.pcf8591.read(channel=1)
            self.__data.outdoor_temp = self.ds1820_outdoor.read_temperature()
            self.__data.water_temp = 0.0
            self.__data.valid = True
            print(self.__data)

    def stop (self):
        self._running = False

# eof #

