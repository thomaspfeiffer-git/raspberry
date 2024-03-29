#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# Wardrobe_UDP.py                                                             #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2019, 2020, 2023       #
###############################################################################

"""
Purpose:
1) Send all data using UDP to my main server.
2) Receive data and store to rrd database.

This lib can be used either standalone as a receiver (2) or
imported to another python program as a sender (1).
"""

import configparser as cfgparser
import os
import socket
import sys

sys.path.append("../libs/")
from Logging import Log
import UDP

CREDENTIALS_UDP_RRD = os.path.expanduser("~/credentials/wardrobe.cred")
CREDENTIALS_UDP_HOMEAUTOMATION = os.path.expanduser("~/credentials/homeautomation.cred")
RRDFILE = os.path.expanduser("~/rrd/databases/wardrobe.rrd")


###############################################################################
# UDP_Sender ##################################################################
class UDP_Sender (object):
    def __init__ (self, credentials):
        self.udp = UDP.Sender(credentials)

    def send (self, data):
        self.udp.send(data)


###############################################################################
# UDP_Receiver ################################################################
class UDP_Receiver (object):
    DS_TEMP1     = "wr_temp1"
    DS_TEMPCPU   = "wr_tempcpu"
    DS_TEMP2     = "wr_temp2"
    DS_HUMI      = "wr_humi"
    DS_LIGHTNESS = "wr_lightness"
    DS_OPEN1     = "wr_open1"
    DS_OPEN2     = "wr_open2"
    DS_OPEN3     = "wr_open3"
    DS_OPEN4     = "wr_open4"
    rrd_template = DS_TEMP1     + ":" + \
                   DS_TEMPCPU   + ":" + \
                   DS_TEMP2     + ":" + \
                   DS_HUMI      + ":" + \
                   DS_LIGHTNESS + ":" + \
                   DS_OPEN1     + ":" + \
                   DS_OPEN2     + ":" + \
                   DS_OPEN3     + ":" + \
                   DS_OPEN4

    def __init__ (self, credentials):
        self.udp = UDP.Receiver(credentials)

    def receive (self):
        import rrdtool
        while True:
            rrd_data = self.udp.receive()
            Log(f"RRD Data received: {rrd_data}")
            try:
                rrdtool.update(RRDFILE, "--template", self.rrd_template, rrd_data)
            except rrdtool.OperationalError:
                Log("Cannot update rrd database: {0[0]} {0[1]}".format(sys.exc_info()))


###############################################################################
# shutdown ####################################################################
def shutdown_application ():
    """cleanup stuff"""
    Log("Stopping application")
    Log("Application stopped")
    sys.exit(0)


###############################################################################
## main #######################################################################
if __name__ == "__main__":
    from Shutdown import Shutdown
    shutdown_application = Shutdown(shutdown_func=shutdown_application)

    udp = UDP_Receiver(CREDENTIALS_UDP_RRD)
    udp.receive()

# eof #

