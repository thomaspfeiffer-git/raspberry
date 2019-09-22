# -*- coding: utf-8 -*-
###############################################################################
# Fan.py                                                                      #
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


###############################################################################
# gpio ########################################################################
class gpio (object):
    def __init__ (self, linux_gpio):
        # TODO: Check hardware - nanopi neo only
        self.__pin = str(linux_gpio)

        o = open("/sys/class/gpio/export", "w"); o.write(self.__pin); o.close()
        time.sleep(0.5)
        o = open("/sys/class/gpio/gpio{}/direction".format(self.__pin), "w"); o.write("out"); o.close()
        # self.off() # TODO needs some work on inheritance
        o = open("/sys/class/gpio/gpio{}/value".format(self.__pin), "w"); o.write("1"); o.close()

    def on (self):
        o = open("/sys/class/gpio/gpio{}/value".format(self.__pin), "w"); o.write("0"); o.close()
        pass

    def off (self):
        o = open("/sys/class/gpio/gpio{}/value".format(self.__pin), "w"); o.write("1"); o.close()
        pass

    def close (self, immediate=False):
        self.off(immediate)
        o = open("/sys/class/gpio/unexport", "w"); o.write(self.__pin); o.close()


###############################################################################
# Fan #########################################################################
class Fan (gpio):
    def __init__ (self, pin, delay=0):
        super().__init__(linux_gpio=pin)
        self.pin = pin
        self.delay = delay

        self.__thread_on = None
        self.__thread_off = None

    def __on (self):
        time.sleep(self.delay)
        super().on()
        Log("Fan {} switched on.".format(self.pin))

    def __off (self, immediate):
        if not immediate:
            time.sleep(self.delay)
        super().off()
        Log("Fan {} switched off.".format(self.pin))

    def on (self):
        if self.__thread_on:
            self.__thread_on.join()
            self.__thread_on = None
        self.__thread_on = threading.Thread(target=self.__on)
        self.__thread_on.start()

    def off (self, immediate=False):
        if self.__thread_off:
            self.__thread_off.join()
            self.__thread_off = None
        self.__thread_off = threading.Thread(target=self.__off, kwargs={'immediate': immediate})
        self.__thread_off.start()

# eof #

