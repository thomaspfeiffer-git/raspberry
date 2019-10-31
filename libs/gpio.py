# -*- coding: utf-8 -*-
##############################################################################
# gpio.py                                                                    #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2019                  #
##############################################################################

import sys
import time

sys.path.append('../libs')
from sensors.Adafruit import Adafruit_GPIO_Platform as Platform

##############################################################################
# gpio #######################################################################
class gpio (object):
    IN  = 'in'
    OUT = 'out'
    def __init__ (self, linux_gpio, direction):
        if Platform.platform_detect() != Platform.NANOPI:
            raise RuntimeError("This library only works on NanoPi NEO Air.")

        self.__pin = "{}".format(linux_gpio)
        if direction != gpio.IN and direction != gpio.OUT:
            raise ValueError("direction must be 'gpio.IN' or 'gpio.OUT'.")

        self.__direction = direction
        o = open("/sys/class/gpio/export", "w")
        o.write(self.__pin)
        o.close()
        time.sleep(0.5)
        o = open("/sys/class/gpio/gpio{}/direction".format(self.__pin), "w")
        o.write(self.__direction)
        o.close()

    def read (self):
        if self.__direction != gpio.IN:
            raise RuntimeError("direction not set to input.")
        o = open("/sys/class/gpio/gpio{}/value".format(self.__pin), "r")
        v = o.read()
        o.close()
        return v

    def write (self, value):
        if self.__direction != gpio.OUT:
            raise RuntimeError("direction not set to output.")
        o = open("/sys/class/gpio/gpio{}/value".format(self.__pin), "w")
        o.write(value)
        o.close()

    def close (self):
        o = open("/sys/class/gpio/unexport", "w"); 
        o.write(self.__pin); 
        o.close()

# eof #

