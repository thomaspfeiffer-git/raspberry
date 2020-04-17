#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# Serverroom_UDP.py                                                           #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2019, 2020             #
###############################################################################

"""
Purpose:
1) Send all data using UDP to my main server.
2) Receive data and store to rrd database.

This lib can be used either standalone as a receiver (2) or
imported to another python program as a sender (1).
"""

import os
import sys
import time

sys.path.append("../libs/")
from Commons import Digest
from Logging import Log
import UDP

CREDENTIALS = os.path.expanduser("~/credentials/serverroom.cred")
RRDFILE = os.path.expanduser("~/rrd/databases/serverroom.rrd")


###############################################################################
# UDP_Sender ##################################################################
class UDP_Sender (UDP.Sender):
    def __init__ (self, credentials_file=CREDENTIALS):
        super().__init__(credentials_file)


###############################################################################
# UDP_Receiver ################################################################
class UDP_Receiver (UDP.Receiver):
    # TODO: move to central place (same code in Serverroom.py)
    DS_TEMP = "temp"
    DS_HUMI = "humi"
    DS_TEMPCPU = "tempcpu"
    rrd_template = DS_TEMP + ":" + \
                   DS_HUMI + ":" + \
                   DS_TEMPCPU

    def __init__ (self, credentials_file):
        super().__init__(credentials_file)

    def receive (self):
        import rrdtool
        while True:
            data = super().receive()
            Log(f"RRD Data received: {data}")
            try:                                      # TODO
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
## main #######################################################################
if __name__ == "__main__":
    from Shutdown import Shutdown
    shutdown_application = Shutdown(shutdown_func=shutdown_application)

    udp = UDP_Receiver(CREDENTIALS)
    udp.receive()

# eof #

