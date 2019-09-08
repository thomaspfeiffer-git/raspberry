#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# Ventilation.py                                                              #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2019                   #
###############################################################################

"""
Controls ventilation of the control room of our swimming pool.
"""

### Usage ###
### TODO


import sys



sys.path.append("../libs/")
from Logging import Log
from Shutdown import Shutdown

from sensors.CPU import CPU
from sensors.DS1820 import DS1820


# temperature and humidity sensor SHT31
# https://github.com/adafruit/Adafruit_CircuitPython_SHT31D
# http://www.pibits.net/code/raspberry-pi-sht31-sensor-example.php
 
# Sensor #1: AirIn
# Sensor #2: AirOut


# Fans (AirIn, AirOut):
# https://www.amazon.de/s?k=l%C3%BCfter+5v+60mm&__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&ref=nb_sb_noss


# Control of fans:
# MCP23017 (max 25 mA sink/source capability per I/O - maybe too less?)




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



# eof #

