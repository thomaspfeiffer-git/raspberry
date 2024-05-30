#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# Watchdog.py                                                                 #
# (c) https://github.com/thomaspfeiffer-git 2024                              #
###############################################################################

"""
Sends pings to various Raspberrys to keep them awake (or reboot).
"""

import datetime
import socket
import sys
import time


sys.path.append("../libs/")
from Logging import Log
from Shutdown import Shutdown


###############################################################################
# UDP #########################################################################
class UDP (object):
    def __init__ (self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.UDP_PORT = 6666

    def ping (self, destination):
        datagram = datetime.datetime.now().strftime('%Y%m%d %H:%M:%S').encode('utf-8')
        try:
            sent = self.socket.sendto(datagram, (destination, self.UDP_PORT))
            Log(f"Sent bytes: {sent}; data: {datagram}")
        except:
            Log("Cannot send data: {0[0]} {0[1]} (Data: {1})".format(sys.exc_info(), datagram))



###############################################################################
###############################################################################
def Sender ():
    udp = UDP()
    while True:
        # read config file
        # send udp paket to hosts
        # udp.ping("10.14.1.77")
        udp.ping("pih")
        for _ in range(600):
            time.sleep(0.01)
            # time.sleep(0.1)


###############################################################################
# Shutdown stuff ##############################################################
def shutdown_application ():
    """cleanup stuff"""
    Log("Stopping application")
    Log("Application stopped")
    sys.exit(0)


###############################################################################
## main #######################################################################
if __name__ == "__main__":
    shutdown_application = Shutdown(shutdown_func=shutdown_application)


    Sender()

# eof #

