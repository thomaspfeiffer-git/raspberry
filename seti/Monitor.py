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

- ... and some more
"""


### usage ###
# nohup ./Monitor.py 2>&1 > monitor.py &


### libraries to be installed ###
# sudo pip3 install psutil


import configparser as cfgparser
import os
import psutil
import socket
import sys
import time


sys.path.append("../libs/")
from Commons import Digest
from Logging import Log
from Shutdown import Shutdown

from sensors.CPU import CPU


# Hosts where this app runs
seti_01 = "seti_01"
seti_02 = "seti_02"
seti_03 = "seti_03"
seti_04 = "seti_04"
PIs = [seti_01, seti_02, seti_03, seti_04]
this_PI = socket.gethostname()


if this_PI == seti_01:
    pass
    # from sensors.DS1820 import DS1820
    # from sensors.BME680 import BME680, BME_680_BASEADDR, BME_680_SECONDARYADDR


CREDENTIALS = "/home/pi/credentials/seti.cred"
cred = cfgparser.ConfigParser()
cred.read(CREDENTIALS)


###############################################################################
# CONFIG ######################################################################
class CONFIG (object):
    SECRET = cred['UDP']['SECRET']
    IP_ADDRESS_SERVER = cred['UDP']['IP_ADDRESS_SERVER']
    UDP_PORT = int(cred['UDP']['UDP_PORT'])
    MAX_PACKET_SIZE = int(cred['UDP']['MAX_PACKET_SIZE'])


###############################################################################
# UDP_Sender ##################################################################
class UDP_Sender (object):
    def __init__ (self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.digest = Digest(CONFIG.SECRET)

    def send (self, data):
        payload = data
        datagram = "{},{}".format(payload,self.digest(payload)).encode('utf-8')
        try:
            sent = self.socket.sendto(datagram, 
                                      (CONFIG.IP_ADDRESS_SERVER, 
                                      CONFIG.UDP_PORT))
            Log("Sent bytes: {}; data: {}".format(sent,datagram))
        except:
            Log("Cannot send data: {0[0]} {0[1]}".format(sys.exc_info()))


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
    udp = UDP_Sender()

    while True:
        cpu_usage = psutil.cpu_percent(percpu=True)
        rrd_data = "N:{:.2f}".format(cpu.read_temperature()) + \
                    ":{:.2f}".format(os.getloadavg()[0])     + \
                    ":{:.2f}".format(psutil.cpu_freq()[0])   + \
                    ":{:.2f}".format(cpu_usage[0])           + \
                    ":{:.2f}".format(cpu_usage[1])           + \
                    ":{:.2f}".format(cpu_usage[2])           + \
                    ":{:.2f}".format(cpu_usage[3])           + \
                    ":{:.2f}".format(-99.01)   + \
                    ":{:.2f}".format(-99.02)   + \
                    ":{:.2f}".format(-99.03)   + \
                    ":{:.2f}".format(-99.04)   + \
                    ":{:.2f}".format(-99.05)   + \
                    ":{:.2f}".format(-99.06)
        # 99.01: V_Temp_Room
        # 99.02: V_Temp_Airflow
        # 99.03: V_Humidity
        # 99.04: reserved; maybe fan speed?
        # 99.05: reserved
        # 99.06: reserved

        # Log("{},{}".format(this_PI,rrd_data))
        udp.send("{},{}".format(this_PI,rrd_data))
        time.sleep(120)

# eof #        

