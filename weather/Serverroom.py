#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# Serverroom.py                                                               #
# Monitors temperature and humidity in our server room                        #
# (c) https://github.com/thomaspfeiffer-git 2020                              #
###############################################################################
""" Collect temperature and humidity in our server room (mainly with HTU21DF). """

"""
##### start with:
### read data from sensor and send to udp server
nohup ./Serverroom.py --sensor 2>&1 >serverroom.log &

### receive data via udp and store in rrd database
nohup ./Serverroom.py --receiver 2>&1 >serverroom_udp.log &
"""

import argparse
import os
import rrdtool
import sys
import time

sys.path.append('../libs')

from sensors.HTU21DF import HTU21DF
from sensors.CPU import CPU

from Logging import Log
from Shutdown import Shutdown
import UDP


# Misc for rrdtool
CREDENTIALS = os.path.expanduser("~/credentials/serverroom.cred")
RRDFILE = os.path.expanduser("~/rrd/databases/serverroom.rrd")
DS_TEMP       = "temp"
DS_HUMI       = "humi"
DS_TEMPCPU    = "tempcpu"


###############################################################################
# Sensor ######################################################################
def Sensor ():
    """reads data from sensor"""
    htu21df = HTU21DF()
    cpu = CPU()
    udp = UDP.Sender(CREDENTIALS)

    while True:
        temperature = htu21df.read_temperature()
        humidity    = htu21df.read_humidity()
        cpu_temp    = cpu.read_temperature()

        rrd_data = "N:" + \
                   ":".join(f"{d:.2f}" for d in [temperature, \
                                                 humidity,   \
                                                 cpu_temp])
        udp.send(rrd_data)
        time.sleep(50)


###############################################################################
# Receiver ####################################################################
def Receiver ():
    rrd_template = DS_TEMP + ":" + \
                   DS_HUMI + ":" + \
                   DS_TEMPCPU
    udp = UDP.Receiver(CREDENTIALS)

    while True:
        data = udp.receive()
        Log(f"RRD Data received: {data}")
        try:
            rrdtool.update(RRDFILE, "--template", rrd_template, data)
        except rrdtool.OperationalError:
            Log("Cannot update rrd database: {0[0]} {0[1]}".format(sys.exc_info()))


###############################################################################
# Exit ########################################################################
def shutdown_application ():
    """cleanup stuff"""
    sys.exit(0)


###############################################################################
# main ########################################################################
if __name__ == '__main__':
    shutdown = Shutdown(shutdown_func=shutdown_application)

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--sensor", help="read data from sensor and send to udp server", action="store_true")
    group.add_argument("--receiver", help="receive data via udp and store in rrd database", action="store_true")
    args = parser.parse_args()

    if args.sensor:
        Sensor()
    if args.receiver:
        Receiver()

# eof #

