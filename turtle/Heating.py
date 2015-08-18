#############################################################################
# Heating.py                                                                #
# Control heating                                                           #
# (c) https://github.com/thomaspfeiffer-git 2015                            #
#############################################################################
"""control heating of our turtle's compound"""

import RPi.GPIO as io
from threading import Lock
from time import time


class Heating:
    ON  = "on"
    OFF = "off" 
    __instances_lock = Lock()
    __instances = 0

    def __off (self):
        """access hardware: switch off"""
        io.output(self.__pin, io.LOW)
        self.__status = self.OFF  


    def __init__ (self, pin, latency, dryrun=False):
        with Heating.__instances_lock:
            Heating.__instances += 1
        self.__pin     = pin
        self.__latency = latency
        self.__dryrun  = dryrun
        self.__lastchanged = 0
        self.__status  = self.OFF

        io.setmode(io.BOARD)
        io.setup(self.__pin, io.OUT)
        self.__off()


    def __delayperiod (self):
        """add latency for switch on/off"""
        __t = time()
        if (__t >= self.__lastchanged + self.__latency): 
            self.__lastchanged = __t
            return True
        else:
            return False


    def status (self):
        if (self.__status == self.ON):
            return 1
        else:
            return 0


    def cleanup (self):
        self.__off()
        if Heating.__instances == 1:
            io.cleanup()
        else:
            with Heating.__instances_lock:
                Heating.__instances -= 1


    def on (self):
        if (self.__status != self.ON):
            if (self.__delayperiod()):
                if (self.__dryrun):
                    print("Dry run: {}".format(self.ON))
                else:
                    io.output(self.__pin, io.HIGH)
                self.__status = self.ON


    def off (self):
        if (self.__status != self.OFF):
            if (self.__delayperiod()):
                self.__off()

### eof ###

