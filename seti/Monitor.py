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


V_Timestamp = "Timestamp"
V_CPU_Temp = "CPU Temperature"
V_CPU_AvgLoad = "CPU AvgLoad"
V_CPU_Usage_Core0 = "CPU Usage Core 0"
V_CPU_Usage_Core1 = "CPU Usage Core 1"
V_CPU_Usage_Core2 = "CPU Usage Core 2"
V_CPU_Usage_Core3 = "CPU Usage Core 3"
V_CPU_Frequency = "CPU Frequency"
V_Temp_Room = "Temperature Room"
V_Temp_Airflow = "Temperature Airflow"
V_Humidity = "Humidity"



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
        cpu_usage = psutil.cpu_percent(percpu=True)
        data = { V_Timestamp: time.strftime("%Y%m%d %H:%M:%S"),
                 V_CPU_Temp: cpu.read_temperature(),
                 V_CPU_AvgLoad: os.getloadavg()[0],
                 V_CPU_Frequency: psutil.cpu_freq()[0],
                 V_CPU_Usage_Core0: cpu_usage[0],
                 V_CPU_Usage_Core1: cpu_usage[1],
                 V_CPU_Usage_Core2: cpu_usage[2],
                 V_CPU_Usage_Core3: cpu_usage[3],
                 V_Temp_Room: "n/a",
                 V_Temp_Airflow: "n/a",
                 V_Humidity: "n/a" }

        print(data)
        time.sleep(10)


# eof #        

