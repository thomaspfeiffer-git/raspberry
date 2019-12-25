#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
############################################################################
# Button.py                                                                #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2017, 2019          #
############################################################################
"""
"""
   

### usage ###
# sudo Button.py

import socket
import sys
import time
import urllib.request

sys.path.append("../libs/")
from gpio import gpio as io
from Logging import Log
from Shutdown import Shutdown

url = "http://localhost:5000/toggle?button=1" # TODO config file
pin = XXX   # Phys pin 10

###############################################################################
# CallToggle ##################################################################
def CallToggle ():
    try:
        response = urllib.request.urlopen(url)
        data = response.read().decode("utf-8")
        Log("toggled!")
    except (IOError):
        Log("Error: {0[0]} {0[1]}".format(sys.exc_info()))
    except socket.timeout:
        Log("socket.timeout: {0[0]} {0[1]}".format(sys.exc_info()))

###############################################################################
# Shutdown stuff ##############################################################
def shutdown_application ():
    """cleanup stuff"""
    Log("Stopping application")
    btn.close()
    Log("Application stopped")
    sys.exit(0)

###############################################################################
## main ######################################################################
if __name__ == "__main__":
    shutdown_application = Shutdown(shutdown_func=shutdown_application)

    btn = io(pin, io.IN)
    last = None
    while True:
        act = int(btn.read())   # TODO: debounce if necessary
        if act != last:
            if last == 1 and act == 0:  # falling edge
                CallToggle()
            last = act

        time.sleep(0.05)

# eof #

