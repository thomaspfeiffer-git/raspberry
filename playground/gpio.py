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
    def __init__ (self, linux_gpio):
        # TODO: Check hardware - nanopi neo only
        self.__pin = "{}".format(linux_gpio)
        o = open("/sys/class/gpio/export", "w"); o.write(self.__pin); o.close()
        time.sleep(0.5)
       o = open("/sys/class/gpio/gpio{}/direction".format(self.__pin), "w"); o.write("out"); o.close()

    def on (self):
        o = open("/sys/class/gpio/gpio{}/value".format(self.__pin), "w"); o.write("1"); o.close()

    def off (self):
        o = open("/sys/class/gpio/gpio{}/value".format(self.__pin), "w"); o.write("0"); o.close()

    def close (self):
        o = open("/sys/class/gpio/unexport", "w"); o.write(self.__pin); o.close()


###############################################################################
# Shutdown stuff ##############################################################
def shutdown_application ():
    """cleanup stuff"""
    Log("Stopping application")
    led1.close()
    led2.close()
    Log("Application stopped")
    sys.exit(0)


###############################################################################
## main #######################################################################
if __name__ == "__main__":
    shutdown_application = Shutdown(shutdown_func=shutdown_application)

    led1 = gpio(65)
    led2 = gpio(66)

    while True:
        led1.on()
        led2.off()
        time.sleep(0.5)
        led1.off()
        led2.on()
        time.sleep(0.5)

# eof #

