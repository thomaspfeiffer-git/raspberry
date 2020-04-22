#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
#############################################################################
# Kidsroom_UDP.py                                                           #
# UDP/RRD client for monitoring temperature and humidity in our kid's room. #
# (c) https://github.com/thomaspfeiffer-git 2020                            #
#############################################################################
"""
UDP/RRD client for monitoring temperature and humidity in our kid's room.
"""

"""
####### usage ######
nohup ./Kidsroom_UDP.py 2>&1 >kidsroom_udp.log &
"""

import os
import rrdtool
import sys

sys.path.append('../libs')

from Logging import Log
from Shutdown import Shutdown
import UDP


# Misc for rrdtool
CREDENTIALS = os.path.expanduser("~/credentials/kidsroom.cred")
RRDFILE = os.path.expanduser("~/rrd/databases/kidsroom.rrd")

DS_TEMP1   = "kidsroom_temp1"
DS_TEMPCPU = "kidsroom_tempcpu"
DS_TEMP2   = "kidsroom_temp2"
DS_HUMI    = "kidsroom_humi"


###############################################################################
# Receiver ####################################################################
def Receiver ():
    rrd_template = DS_TEMP1   + ":" + \
                   DS_TEMPCPU + ":" + \
                   DS_TEMP2   + ":" + \
                   DS_HUMI
    udp = UDP.Receiver(CREDENTIALS)

    while True:
        rrd_data = udp.receive()
        Log(f"RRD Data received: {rrd_data}")
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
###############################################################################
if __name__ == '__main__':
    shutdown = Shutdown(shutdown_func=shutdown_application)

    Receiver()

### eof ###

