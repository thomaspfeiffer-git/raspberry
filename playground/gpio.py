#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
##############################################################################
# gpio.py                                                                    #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2019                  #
##############################################################################


#####


import sys
import time

sys.path.append('../libs')

from Logging import Log
from Shutdown import Shutdown


class gpio (object):
    IN  = 'in'
    OUT = 'out'
    def __init__ (self, linux_gpio, direction):
        # TODO: Check hardware - nanopi neo only
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
            raise RuntimeError("direction not set to input")
        o = open("/sys/class/gpio/gpio{}/value".format(self.__pin), "r")
        v = o.read()
        o.close()
        return v

    def write (self, value):
        if self.__direction != gpio.OUT:
            raise RuntimeError("direction not set to output")
        o = open("/sys/class/gpio/gpio{}/value".format(self.__pin), "w")
        o.write(value)
        o.close()

    def close (self):
        o = open("/sys/class/gpio/unexport", "w"); 
        o.write(self.__pin); 
        o.close()


###############################################################################
# Shutdown stuff ##############################################################
def shutdown_application ():
    """cleanup stuff"""
    Log("Stopping application")
    inp.close()
    led1.close()
    led2.close()
    Log("Application stopped")
    sys.exit(0)


###############################################################################
## main #######################################################################
if __name__ == "__main__":
    shutdown_application = Shutdown(shutdown_func=shutdown_application)

    led1 = gpio(65, gpio.OUT)
    led2 = gpio(66, gpio.OUT)
    inp  = gpio(67, gpio.IN)

    x = inp.read()
    print("x: {}".format(x))

    while True:
        led1.write("1")
        led2.write("0")
        time.sleep(0.5)
        led1.write("0")
        led2.write("1")
        time.sleep(0.5)

# eof #
