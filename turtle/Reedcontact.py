#############################################################################
# Reedcontact.py                                                            #
# (c) https://github.com/thomaspfeiffer-git 2015                            #
#############################################################################
"""Provides some functionality for a reed contact"""

import RPi.GPIO as io
from time import time, strftime, localtime, sleep
import threading


class Reedcontact (threading.Thread):
    def __init__ (self, pin, stretch):
        threading.Thread.__init__(self)

        self.__pin = pin
        self.__status = False
        self.__stretch = stretch
        self.__timestretched = time()

        io.setmode(io.BOARD)
        io.setup(self.__pin, io.IN)
        io.setup(self.__pin, io.IN, pull_up_down=io.PUD_UP)  

        self.__running = True


    def run(self):
        i = 0
        while (self.__running):
            if (io.input(self.__pin)):
                i += 1
            else:
                i = 0
                self.__status = False

            if (i >= 10):
                self.__status = True
                self.__timestretched = time() + self.__stretch
                i = 10 # avoid overflow
            sleep(1)


    def stop(self):
        self.__running = False


    def cleanup (self):
        """do some cleanup on io"""
        self.stop()


    def status (self):
        """return status of reedcontact"""
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

