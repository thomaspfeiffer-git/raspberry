# -*- coding: utf-8 -*-
###############################################################################
# Fan.py                                                                      #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2019, 2020             #
###############################################################################

"""
TODO
"""

import sys
import threading
import time

sys.path.append("../libs/")
from gpio import gpio as io
from Logging import Log


###############################################################################
# gpio ########################################################################
class gpio (object):
    def __init__ (self, pin):
        self.__io = io(pin, io.OUT)

    def on (self):
        self.__io.write("0")

    def off (self):
        self.__io.write("1")

    def close (self, immediate=False):
        self.off(immediate)
        self.__io.close()


###############################################################################
# Fan #########################################################################
class Fan (gpio):
    def __init__ (self, pin, delay=0):
        super().__init__(pin=pin)
        self.pin = pin
        self.delay = delay

        self.__thread_on = None
        self.__thread_off = None

        self.off(immediate=True)

    def __on (self):
        time.sleep(self.delay)
        super().on()
        Log(f"Fan {self.pin} switched on.")

    def __off (self, immediate):
        if not immediate:
            time.sleep(self.delay)
        super().off()
        Log(f"Fan {self.pin} switched off.")

    def on (self):
        if self.__thread_on:
            self.__thread_on.join()
            self.__thread_on = None
        self.__thread_on = threading.Thread(target=self.__on)
        self.__thread_on.start()

    def off (self, immediate=False):
        if not immediate:
            if self.__thread_off:
                self.__thread_off.join()
                self.__thread_off = None
            self.__thread_off = threading.Thread(target=self.__off, kwargs={'immediate': immediate})
            self.__thread_off.start()
        else:    
            super().off()
            Log(f"Fan {self.pin} switched off immediately.")

# eof #

