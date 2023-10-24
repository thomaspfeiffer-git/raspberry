#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# Indoor.py                                                                   #
# Monitors temperature, humidity, and air pressure in our living room.        #
# (c) https://github.com/thomaspfeiffer-git 2019, 2020, 2022, 2023            #
###############################################################################
""" Collect weather and some other data indoor (mainly with BME680). """

"""
##### start with:
### read data from sensor and send to udp server
nohup ./Indoor.py --sensor 2>&1 >indoor.log &

### receive data via udp and store in rrd database
nohup ./Indoor.py --receiver 2>&1 >indoor_udp.log &
"""

import argparse
import os
import rrdtool
import sys
import time

sys.path.append('../libs')

from sensors.BME680 import BME680, BME_680_BASEADDR
from sensors.CPU import CPU

from Logging import Log
from Shutdown import Shutdown
import UDP


CREDENTIALS_UDP_RRD = os.path.expanduser("~/credentials/weather_indoor.cred")
CREDENTIALS_UDP_HOMEAUTOMATION = os.path.expanduser("~/credentials/homeautomation.cred")

RRDFILE       = os.path.expanduser("~/rrd/databases/weather_indoor.rrd")
DS_TEMP       = "temp"
DS_HUMI       = "humi"
DS_PRESSURE   = "pressure"
DS_AIRQUALITY = "airquality"
DS_TEMPCPU    = "temp_cpu"


###############################################################################
# Sensor ######################################################################
def Sensor ():
    bme680 = BME680(i2c_addr=BME_680_BASEADDR)
    cpu = CPU()
    udp_rrd = UDP.Sender(CREDENTIALS_UDP_RRD)
    udp_homeautomation = UDP.Sender(CREDENTIALS_UDP_HOMEAUTOMATION)

    while True:
        bme680.get_sensor_data()
        temp       = bme680.data.temperature
        humi       = bme680.data.humidity
        pressure   = bme680.data.pressure
        airquality = bme680.data.air_quality_score \
                     if bme680.data.air_quality_score != None else 0
        cpu_temp   = cpu.read_temperature()

        rrd_data = "N:" + \
                   ":".join(f"{d:.2f}" for d in [temp,       \
                                                 humi,       \
                                                 pressure,   \
                                                 airquality, \
                                                 cpu_temp])

        udp_rrd.send(rrd_data)
        udp_homeautomation.send(f"Weather_Indoor - {rrd_data}")
        time.sleep(50)


###############################################################################
# Receiver ####################################################################
def Receiver ():
    rrd_template = DS_TEMP       + ":" + \
                   DS_HUMI       + ":" + \
                   DS_PRESSURE   + ":" + \
                   DS_AIRQUALITY + ":" + \
                   DS_TEMPCPU
    udp = UDP.Receiver(CREDENTIALS_UDP_RRD)

    while True:
        try:
            data = udp.receive()
        except DatagramError:
            Log("Datagram error")
        else:
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

