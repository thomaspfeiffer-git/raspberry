#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
##############################################################################
# Sensors_UDP.py                                                             #
# (c) https://github.com/thomaspfeiffer-git 2020                             #
##############################################################################
"""
TODO
"""

"""
### usage ###
TODO
"""

import os
import rrdtool
import sys

sys.path.append('../../libs')
from Logging import Log
from Shutdown import Shutdown
import UDP


# Misc for rrdtool
CREDENTIALS = os.path.expanduser("~/credentials/kitchen.cred") # TODO
RRDFILE = os.path.expanduser("~/rrd/databases/kitchen.rrd")
DS_TEMP        = "ki_temp"
DS_TEMPCPU     = "ki_tempcpu"
DS_HUMI        = "ki_humi"
DS_AIRPRESSURE = "ki_pressure"
DS_LIGHTNESS   = "ki_lightness"
DS_AIRQUALITY  = "ki_airquality"
DS_OPEN1       = "ki_open1"
DS_OPEN2       = "ki_open2"
DS_OPEN3       = "ki_open3"
DS_OPEN4       = "ki_open4"


###############################################################################
# Receiver ####################################################################
def Receiver ():
    rrd_template = DS_TEMP        + ":" + \
                   DS_TEMPCPU     + ":" + \
                   DS_HUMI        + ":" + \
                   DS_AIRPRESSURE + ":" + \
                   DS_LIGHTNESS   + ":" + \
                   DS_AIRQUALITY  + ":" + \
                   DS_OPEN1       + ":" + \
                   DS_OPEN2       + ":" + \
                   DS_OPEN3       + ":" + \
                   DS_OPEN4
    udp = UDP.Receiver(CREDENTIALS)

    while True:
        rrd_data = udp.receive()
        Log(f"RRD data received: {rrd_data}")
        try:
            rrdtool.update(RRDFILE, "--template", rrd_template, rrd_data)
        except rrdtool.OperationalError:
            Log("Cannot update rrd database: {0[0]} {0[1]}".format(sys.exc_info()))


###############################################################################
# Exit ########################################################################
def shutdown_application ():
    """cleanup stuff"""
    Log("Stopping application")
    Log("Application stopped")
    sys.exit(0)


###############################################################################
# Main ########################################################################
if __name__ == '__main__':
    shutdown = Shutdown(shutdown_func=shutdown_application)
    Receiver()

# eof #

