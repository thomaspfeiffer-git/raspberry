#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
#############################################################################
# Weather_Kollerberg.py                                                     #
# (c) https://github.com/thomaspfeiffer-git 2020                            #
#############################################################################
"""Weather station at our summer cottage"""

"""
###### usage #####
### read data from sensor and send to udp server
nohup ./Weather_Kollerberg.py --sensor 2>&1 >weather_kollerberg.log &

### receive data via udp and store in rrd database
nohup ./Weather_Kollerberg.py --receiver_rrd 2>&1 >weather_kollerberg_rrd.log &

### receive data via udp and send to homeautomation server
nohup ./Weather_Kollerberg.py --receiver_homeautomation 2>&1 >weather_kollerberg_homeautomation.log &
"""

import argparse
import os
import socket
import sys
import time

sys.path.append('../libs')

from sensors.CPU import CPU
from sensors.HTU21DF import HTU21DF
from sensors.DS1820 import DS1820

from Logging import Log
from Shutdown import Shutdown
import UDP


# Hosts where this app runs
pik_i = "pik-i"
pik_a = "pik-a"
pik_k = "pik-k"
PIs = [pik_i, pik_a, pik_k]
this_PI = socket.gethostname()

if this_PI == pik_i:   # BME680 installed only at pik_i
    from sensors.BME680 import BME680, BME_680_SECONDARYADDR


AddressesDS1820 = { pik_i: "/sys/bus/w1/devices/w1_bus_master1/28-000006de80e2/w1_slave",
                    pik_a: "/sys/bus/w1/devices/w1_bus_master1/28-000006dd6ac1/w1_slave",
                    pik_k: "/sys/bus/w1/devices/w1_bus_master1/28-000006de535b/w1_slave" }


# Misc for rrdtool
CREDENTIALS_RRD = os.path.expanduser("~/credentials/weather_kollerberg_rrd.cred")
CREDENTIALS_HA = os.path.expanduser("~/credentials/weather_kollerberg_ha.cred")
DS_TEMP1 = "DS_TEMP1"
DS_TEMP2 = "DS_TEMP2"
DS_TCPU  = "DS_TCPU"
DS_HUMI  = "DS_HUMI"
DS_PRESS = "DS_PRESS"
DS_AIRQ  = "DS_AIRQ"


###############################################################################
# Sensor ######################################################################
def Sensor ():
    """reads data from sensor"""

    if this_PI not in PIs:
        Log("wrong host!")
        global shutdown_application
        shutdown_application()

    tempds  = DS1820(AddressesDS1820[this_PI])
    tempcpu = CPU()
    if this_PI == pik_i:
        bme680 = BME680(i2c_addr=BME_680_SECONDARYADDR)
    else:
        htu21df = HTU21DF()

    udp_rrd = UDP.Sender(CREDENTIALS_RRD)  # Server for all rrd stuff
    udp_ha = UDP.Sender(CREDENTIALS_HA)    # Display at home ("Homeautomation")

    pressure = 1013.25 # in case of no BME680 available
    airquality = 0

    while True:
        temp_ds  = tempds.read_temperature()
        temp_cpu = tempcpu.read_temperature()

        if this_PI == pik_i:
            bme680.get_sensor_data()
            temp = bme680.data.temperature
            humi = bme680.data.humidity
            pressure = bme680.data.pressure
            airquality = bme680.data.air_quality_score \
                         if bme680.data.air_quality_score != None else 0
        else:
            temp = htu21df.read_temperature()
            humi = htu21df.read_humidity()

        rrd_data = "N:{:.2f}".format(temp_ds)     + \
                    ":{:.2f}".format(temp)    + \
                    ":{:.2f}".format(temp_cpu)    + \
                    ":{:.2f}".format(humi)    + \
                    ":{:.2f}".format(pressure) + \
                    ":{:.2f}".format(airquality)

        udp_rrd.send(f"{this_PI},{rrd_data}")
        udp_ha.send(f"{this_PI},{rrd_data}")
        time.sleep(45)


###############################################################################
# Receiver_RRD ################################################################
def Receiver_RRD ():
    pass


###############################################################################
# Receiver_Homeautomation #####################################################
def Receiver_Homeautomation ():
    pass


###############################################################################
# Exit ########################################################################
def shutdown_application ():
    """cleanup stuff"""
    Log("Stopping application")
    Log("Application stopped")
    sys.exit(0)


###############################################################################
# main ########################################################################
if __name__ == '__main__':
    shutdown_application = Shutdown(shutdown_func=shutdown_application)

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--sensor", help="read data from sensor and send to udp server", action="store_true")
    group.add_argument("--receiver_rrd", help="receive data via udp and store in rrd database", action="store_true")
    group.add_argument("--receiver_homeautomation", help="receive data via udp and send to homeautomation server", action="store_true")
    args = parser.parse_args()

    if args.sensor:
        Sensor()
    if args.receiver_rrd:
        Receiver_RRD()
    if args.receiver_homeautomation:
        Receiver_Homeautomation()

# eof #

### eof ###

