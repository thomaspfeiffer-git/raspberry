#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# Anteroom_UDP.py                                                             #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2020                   #
###############################################################################
"""
TODO
"""

"""
###### usage ######
a) imported as libary in Anteroom.py
b) standalone as UDP receiver:
nohup ./Anteroom_UDP.py 2>&1 > anteroom_udp.log &
"""

import os
import rrdtool
import sys

sys.path.append('../libs')
from Logging import Log
from Shutdown import Shutdown
import UDP

CREDENTIALS = os.path.expanduser("~/credentials/anteroom.cred")
RRDFILE     = os.path.expanduser("~/rrd/databases/anteroom.rrd")
DS_SWITCH   = "ar_switch"
DS_TEMPCPU  = "ar_tempcpu"
DS_TEMP     = "ar_temp"
DS_HUMI     = "ar_humi"
DS_RES1     = "ar_res1"
DS_RES2     = "ar_res2"
DS_RES3     = "ar_res3"

###############################################################################
# Sender ######################################################################
class Sender (object):
    def __init__ (self):
        self.udp = UDP.Sender(CREDENTIALS)

    def send (self, data):
        self.udp.send(data)


###############################################################################
# Receiver ####################################################################
class Receiver (object):
    rrd_template = DS_SWITCH  + ":" + \
                   DS_TEMPCPU + ":" + \
                   DS_TEMP    + ":" + \
                   DS_HUMI    + ":" + \
                   DS_RES1    + ":" + \
                   DS_RES2    + ":" + \
                   DS_RES3

    def __init__ (self):
        self.udp = UDP.Receiver(CREDENTIALS)

    def run (self):
        while True:
            data = self.udp.receive()
            Log(f"RRD Data received: {data}")
            try:
                rrdtool.update(RRDFILE, "--template", self.rrd_template, data)
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
# main ########################################################################
if __name__ == '__main__':
    shutdown_app = Shutdown(shutdown_func=shutdown_application)

    r = Receiver()
    r.run()

# eof #

