#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# serverroom.py                                                               #
# Monitors temperature and humidity in our server room                        #
# (c) https://github.com/thomaspfeiffer-git 2020                              #
###############################################################################
""" Collect temperature and humidity in our server room (mainly with HTU21DF). """

# start with:
# nohup ./serverroom.py 2>&1 >serverroom.log &

import rrdtool
import sys
import time

sys.path.append('../libs')

from sensors.HTU21DF import HTU21DF
from sensors.CPU import CPU

from Logging import Log
from Shutdown import Shutdown
from Serverroom_UDP import UDP_Sender


# Misc for rrdtool
DATAFILE      = "/schild/weather/serverroom.rrd"
DS_TEMP       = "temp"
DS_HUMI       = "humi"
DS_TEMPCPU    = "tempcpu"


###############################################################################
# Main ########################################################################
def main():
    """main part"""
    htu21df = HTU21DF()
    cpu = CPU()
    udp = UDP_Sender()

    rrd_template = DS_TEMP + ":" + \
                   DS_HUMI + ":" + \
                   DS_TEMPCPU

    while True:
        temperature = htu21df.read_temperature()
        humidity    = htu21df.read_humidity()
        cpu_temp    = cpu.read_temperature()

        rrd_data = "N:" + \
                   ":".join(f"{d:.2f}" for d in [temperature, \
                                                 humidity,   \
                                                 cpu_temp])

        # Log(rrd_template)
        Log(rrd_data)
        udp.send(rrd_data)
        try:
            rrdtool.update(DATAFILE, "--template", rrd_template, rrd_data)
        except rrdtool.OperationalError:
            Log("Cannot update rrd database: {0[0]} {0[1]}".format(sys.exc_info()))

        time.sleep(50)


###############################################################################
# Exit ########################################################################
def shutdown_application ():
    """cleanup stuff"""
    sys.exit(0)


###############################################################################
###############################################################################
if __name__ == '__main__':
    shutdown = Shutdown(shutdown_func=shutdown_application)

    main()

# eof #

