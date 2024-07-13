#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# Boiler.py                                                                   #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2024                   #
###############################################################################

"""
"""

### Usage ###
nohup ./Boiler --duration 3 &
nohup ./Boiler --start 14 --duration 3 &

### Packages you might need to install ###
# sudo apt install python3-gpiozero


import argparse
from datetime import datetime, timedelta
from gpiozero import Button, LED
import sys
import time


sys.path.append("../libs/")
from Logging import Log
from Shutdown import Shutdown



### TODO: Log to permant file



###############################################################################
# CONFIG ######################################################################
class CONFIG:
    class Boiler:
        pin = "BOARD18"



###############################################################################
# Relais ######################################################################
class Relais (object):
    def __init__ (self, pin):
        self.__relais = LED(pin)

    def on (self):
        self.__relais.on()

    def off (self):
        self.__relais.off()


###############################################################################
# Shutdown stuff ##############################################################
def shutdown_application ():
    """cleanup stuff"""
    Log("Stopping application")
    Log("Application stopped")
    sys.exit(0)


###############################################################################
## main #######################################################################
if __name__ == "__main__":
    shutdown_application = Shutdown(shutdown_func=shutdown_application)

    boiler = Relais(CONFIG.Boiler.pin)
    boiler.on()
    time.sleep(5)
    boiler.off()


# eof #

