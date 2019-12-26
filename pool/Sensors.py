# -*- coding: utf-8 -*-
###############################################################################
# Sensors.py                                                                  #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2019                   #
###############################################################################

"""
Contains all sensor stuff.
"""

import sys
import threading
import time


sys.path.append("../libs/")

from Logging import Log

from sensors.CPU import CPU
from sensors.BME280 import BME280
from sensors.DS1820 import DS1820
from sensors.PCF8591 import PCF8591
from sensors.SHT31 import SHT31, SHT31_BASEADDR, SHT31_SECONDARYADDR


###############################################################################
# Sensordata ##################################################################
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
        self.outdoor_temp = None
        self.water_temp = None
        self.fan1_on = 0
        self.fan2_on = 0
        self.fan3_on = 0
        self.fan4_on = 0
        self.engine_circulation = None
        self.engine_countercurrent = None

    def __str__ (self):
        if self.valid:
            return "CPU:          {0.cpu:.2f} C\n"               \
                   "Temp box:     {0.box_temp:.2f} C\n"          \
                   "Temp air in:  {0.airin_temp:.2f} C\n"        \
                   "Temp air out: {0.airout_temp:.2f} C\n"       \
                   "Temp outdoor: {0.outdoor_temp:.2f} C\n"      \
                   "Temp water:   {0.water_temp:.2f} C\n"        \
                   "Humi box:     {0.box_humidity:.2f} % rF\n"    \
                   "Humi air in:  {0.airin_humidity:.2f} % rF\n"  \
                   "Humi air out: {0.airout_humidity:.2f} % rF\n" \
                   "Fan 1 on:     {0.fan1_on}\n"                  \
                   "Fan 2 on:     {0.fan2_on}\n"                  \
                   "Fan 3 on:     {0.fan3_on}\n"                  \
                   "Fan 4 on:     {0.fan4_on}\n"                  \
                   "Engine circulation:     {0.engine_circulation:.2f}\n"    \
                   "Engine counter current: {0.engine_countercurrent:.2f}\n" \
                   .format(self)
        else:
            return "Sensordata not valid."

    @property
    def rrd (self):
        if self.valid:
            return "N:{0.cpu:.2f}"                   \
                    ":{0.box_temp:.2f}"              \
                    ":{0.airin_temp:.2f}"            \
                    ":{0.airout_temp:.2f}"           \
                    ":{0.outdoor_temp:.2f}"          \
                    ":{0.water_temp:.2f}"            \
                    ":{0.box_humidity:.2f}"          \
                    ":{0.airin_humidity:.2f}"        \
                    ":{0.airout_humidity:.2f}"       \
                    ":{0.fan1_on}"                   \
                    ":{0.fan2_on}"                   \
                    ":{0.fan3_on}"                   \
                    ":{0.fan4_on}"                   \
                    ":{0.engine_circulation:.2f}"    \
                    ":{0.engine_countercurrent:.2f}" \
                    .format(self)
        else:
            return "Sensordata not valid."

    @staticmethod
    def rrd_template ():
        return "TEMPCPU:"     \
               "TEMPBOX:"     \
               "TEMPAIRIN:"   \
               "TEMPAIROUT:"  \
               "TEMPOUTDOOR:" \
               "TEMPWATER:"   \
               "HUMIBOX:"     \
               "HUMIAIRIN:"   \
               "HUMIAIROUT:"  \
               "FAN1:"        \
               "FAN2:"        \
               "FAN3:"        \
               "FAN4:"        \
               "ENGCIRC:"     \
               "ENGCC"


###############################################################################
# Sensors #####################################################################
class Sensors (threading.Thread):
    def __init__ (self, data, update_display):
        threading.Thread.__init__(self)

        self.cpu = CPU()
        self.ds1820_water = DS1820("/sys/bus/w1/devices/28-000008561957/w1_slave")
        self.ds1820_outdoor = DS1820("/sys/bus/w1/devices/28-0000085607ec/w1_slave")
        self.bme280_box = BME280()
        self.sht31_airin = SHT31(addr=SHT31_BASEADDR)
        self.sht31_airout = SHT31(addr=SHT31_SECONDARYADDR)
        self.pcf8591 = PCF8591()

        self.__data = data
        self.update_display = update_display
        self._running = True

    def run (self):
       while self._running:
            self.__data.cpu = self.cpu.read_temperature()
            self.__data.box_temp = self.bme280_box.read_temperature()
            self.__data.box_humidity = self.bme280_box.read_humidity()
            self.__data.airin_temp = self.sht31_airin.read_temperature()
            self.__data.airin_humidity = self.sht31_airin.read_humidity()
            self.__data.airout_temp = self.sht31_airout.read_temperature()
            self.__data.airout_humidity = self.sht31_airout.read_humidity()
            self.__data.engine_circulation = self.pcf8591.read(channel=0)
            self.__data.engine_countercurrent = self.pcf8591.read(channel=1)
            self.__data.outdoor_temp = self.ds1820_outdoor.read_temperature()
            self.__data.water_temp = self.ds1820_water.read_temperature()
            self.__data.valid = True
            Log("\n{}".format(self.__data))
            self.update_display()

            for _ in range(600):      # interruptible sleep 
                if not self._running:
                    break
                time.sleep(0.1)

    def stop (self):
        self._running = False

# eof #

