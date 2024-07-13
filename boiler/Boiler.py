#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# Boiler.py                                                                   #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2024                   #
###############################################################################

"""
"""

### Usage ###
# nohup ./Boiler --duration 118 &
# nohup ./Boiler --start 14 --duration 118 &

### Packages you might need to install ###
# sudo apt install python3-gpiozero


import argparse
from datetime import datetime, timedelta
from gpiozero import Button, LED
import sys
import time


sys.path.append("../libs/")
from Shutdown import Shutdown


###############################################################################
# CONFIG ######################################################################
class CONFIG:
    class Boiler:
        pin = "BOARD18"
    class Logging:
        file = "boiler.log"


###############################################################################
# MyLogging ###################################################################
class MyLogging (object):

    def __init__ (self):
        pass

    def __call__ (self, logstr):
        self.Log(logstr)

    def Log (self, logstr):
        import Logging

        Logging.Log(logstr)
        with open(CONFIG.Logging.file, mode='a') as logfile:
            Logging.Log(logstr, logfile)


###############################################################################
# Relais ######################################################################
class Relais (object):
    def __init__ (self, pin):
        self.__relais = LED(pin)

    def on (self):
        self.__relais.on()
        MyLogging("Switched boiler on.")

    def off (self):
        self.__relais.off()
        MyLogging("Switched boiler off.")


###############################################################################
# Shutdown stuff ##############################################################
def shutdown_application ():
    """cleanup stuff"""
    MyLogging.Log("Stopping application")
    boiler.off()
    MyLogging("Application stopped")
    sys.exit(0)


###############################################################################
## main #######################################################################
if __name__ == "__main__":
    shutdown_application = Shutdown(shutdown_func=shutdown_application)
    MyLogging = MyLogging()
    boiler = Relais(CONFIG.Boiler.pin)

    parser = argparse.ArgumentParser()
    parser.add_argument("--duration", "-d", nargs=1, type=int, default=[118],
                        help="Duration in minutes the boiler shall heat.")
    parser.add_argument("--start", "-s", nargs=1, type=int,
                        help="Time of day (hour) the boiler shall be switched on.")
    args = parser.parse_args()
    MyLogging(args)


    """
    if args.start == None:
        boiler.on()
        #schedule boiler.off()
    """
    boiler.on()
    time.sleep(5)
    boiler.off()


# eof #

