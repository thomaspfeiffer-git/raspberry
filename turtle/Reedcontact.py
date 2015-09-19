#############################################################################
# Reedcontact.py                                                            #
# (c) https://github.com/thomaspfeiffer-git 2015                            #
#############################################################################
"""Provides some functionality for a reed contact"""

import RPi.GPIO as io
from time import time


class Reedcontact (object):
    def __init__ (self, pin, stretch):
        self.__pin = pin
        self.__status = False
        self.__stretch = stretch
        self.__timestretched = time()

        def ___callback (pin):
            if (io.input(pin)): 
                self.__status = True
            else:
                self.__status = False
                self.__timestretched = time() + self.__stretch

        io.setmode(io.BOARD)
        io.setup(self.__pin,io.IN)
        io.add_event_detect(self.__pin,io.BOTH)
        io.add_event_callback(self.__pin,___callback)
        io.setup(self.__pin, io.IN, pull_up_down=io.PUD_UP)  


    def cleanup (self):
        io.remove_event_detect(self.__pin)


    def status (self):
        return 1 if self.__status else 0


    def status_stretched (self):
        """enlarge interval of being "on"; otherwise if door is only 
           opened for a short period of time, it would not be seen in RRD"""
        if (self.__status):
            return 1
        else:
            if (time() <= self.__timestretched):
                return 1
            else:
                return 0
              
### eof ###

