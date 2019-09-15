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
# Fan #########################################################################
class Fan (object):
    def __init__ (self, pin, delay=0):
        self.pin = pin
        self.delay = delay

        self.__t_on = None
        self.__t_off = None

    def __on (self):
        time.sleep(self.delay)
        Log("Fan {} switched on.".format(self.pin))

    def __off (self):
        time.sleep(self.delay)
        Log("Fan {} switched off.".format(self.pin))

    def on (self):
        if self.__t_on:
            self.__t_on.join()
        self.__t_on = threading.Thread(target=self.__on)
        self.__t_on.start()

    def off (self):
        if self.__t_off:
            self.__t_off.join()
        self.__t_off = threading.Thread(target=self.__off)
        self.__t_off.start()

# eof #

