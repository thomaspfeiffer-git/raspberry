#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# Relais.py                                                                   #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2017, 2019             #
###############################################################################
"""control lighting of our anteroom:
   check relais and send status to Anteroom main programm"""

### usage ###
# sudo Relais.py

import socket
import sys
import time
import urllib.request

sys.path.append("../libs/")
from gpio import gpio as io
from Logging import Log
from Shutdown import Shutdown

url = "http://localhost:5000/relais?status={}" # TODO config file
pin = 67   # Phys pin 24

###############################################################################
# SendRelaisStatus ############################################################
def SendRelaisStatus (status):
    url_ = url.format(status)

    try:
        response = urllib.request.urlopen(url_)
        data = response.read().decode("utf-8")
    except (IOError):
        Log("Error: {0[0]} {0[1]}".format(sys.exc_info()))
    except socket.timeout:
        Log("socket.timeout: {0[0]} {0[1]}".format(sys.exc_info()))

###############################################################################
# Shutdown stuff ##############################################################
def shutdown_application ():
    """cleanup stuff"""
    Log("Stopping application")
    relais.close()
    Log("Application stopped")
    sys.exit(0)

###############################################################################
## main #######################################################################
if __name__ == "__main__":
    shutdown_application = Shutdown(shutdown_func=shutdown_application)

    relais = io(pin, io.IN)
    last = None
    while True:
        act = int(relais.read())
        if act != last:
            if act == 1:
                SendRelaisStatus("off")
            else:
                SendRelaisStatus("on")

            last = act

        time.sleep(0.05)

# eof #

