#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# Outdoor.py                                                                  #
# Monitors temperature, humidity, and air pressure outside                    #
# (c) https://github.com/thomaspfeiffer-git 2019, 2020, 2023                  #
###############################################################################
""" Collect weather and some other data outdoor. """

"""
### read data from sensor and send to udp server
nohup ./Outdoor.py --sensor 2>&1 >outdoor.log &

### receive data via udp and store in rrd database
nohup ./Outdoor.py --receiver 2>&1 >outdoor_udp.log &
"""

import argparse
import os
import rrdtool
import sys
import time

sys.path.append('../libs')

from sensors.BME280 import BME280
from sensors.CPU import CPU
from sensors.DS1820 import DS1820
from sensors.TSL2561 import TSL2561

from Logging import Log
from Shutdown import Shutdown
import UDP

CREDENTIALS_UDP_RRD = os.path.expanduser("~/credentials/weather_outdoor.cred")
CREDENTIALS_UDP_HOMEAUTOMATION = os.path.expanduser("~/credentials/homeautomation.cred")

RRDFILE       = os.path.expanduser("~/rrd/databases/weather_outdoor.rrd")
DS_TEMP        = "temp"
DS_TEMP_GARDEN = "temp_gard"
DS_HUMI        = "humi"
DS_PRESSURE    = "pressure"
DS_LIGHTNESS   = "lightness"
DS_TEMPCPU     = "temp_cpu"


###############################################################################
# Sensor ######################################################################
def Sensor ():
    """ reads data from sensor(s). """
    bme280 = BME280()
    ds1820 = DS1820("/sys/bus/w1/devices/28-000006d62eb1/w1_slave")
    tsl2561 = TSL2561()
    cpu = CPU()
    udp_rrd = UDP.Sender(CREDENTIALS_UDP_RRD)
    udp_homeautomation = UDP.Sender(CREDENTIALS_UDP_HOMEAUTOMATION)

    while True:
        temp        = bme280.read_temperature()
        temp_garden = temp
        # temp_garden = ds1820.read_temperature()
        humi        = bme280.read_humidity()
        pressure    = bme280.read_pressure()/100.0
        lightness   = tsl2561.lux()
        cpu_temp    = cpu.read_temperature()

        rrd_data = "N:" + \
                   ":".join(f"{d:.2f}" for d in [temp,        \
                                                 temp_garden, \
                                                 humi,        \
                                                 pressure,    \
                                                 lightness,   \
                                                 cpu_temp])
        udp_rrd.send(rrd_data)
        udp_homeautomation.send(f"Weather_Outdoor - {rrd_data}")
        time.sleep(50)


###############################################################################
# Receiver ####################################################################
def Receiver ():
    rrd_template = DS_TEMP        + ":" + \
                   DS_TEMP_GARDEN + ":" + \
                   DS_HUMI        + ":" + \
                   DS_PRESSURE    + ":" + \
                   DS_LIGHTNESS   + ":" + \
                   DS_TEMPCPU
    udp = UDP.Receiver(CREDENTIALS_UDP_RRD)

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
###############################################################################
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

