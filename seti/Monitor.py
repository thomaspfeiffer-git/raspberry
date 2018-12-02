#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# Monitor.py                                                                  #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2019                   #
###############################################################################

"""
Monitoring some data on the seti hardware:
- CPU Load
- CPU Temperature

- Room temperature
- Room humidity
- Airflow temperature
"""

""" 
libraries to be installed:
- sudo pip3 install psutil

"""


import os
import psutil
import sys
import time


sys.path.append("../libs/")
from Logging import Log
from Shutdown import Shutdown

from sensors.CPU import CPU


###############################################################################
## Shutdown stuff #############################################################
def shutdown_application ():
    """cleanup stuff"""
    Log("Stopping application")
    Log("Application stopped")
    sys.exit(0)


###############################################################################
## main #######################################################################
if __name__ == "__main__":
    shutdown_application = Shutdown(shutdown_func=shutdown_application)
    cpu = CPU()

    while True:
        Log(cpu.read_temperature())
        Log(psutil.cpu_percent(percpu=True))
        Log(psutil.cpu_freq())
        Log(psutil.sensors_temperatures())
        Log(os.getloadavg()[0])
        print("")
        time.sleep(10)


# eof #        

