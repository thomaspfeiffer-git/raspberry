#!/usr/bin/python -u
# -*- coding: utf-8 -*-
############################################################################
# Relais.py                                                                #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2017                #
############################################################################
"""control lighting of our anteroom:
   check relais and send status to Anteroom main programm"""

### usage ###
# sudo Relais.py

import RPi.GPIO as io
import socket
import sys
import time
import urllib

sys.path.append("../libs/")
from Logging import Log


pin_ir = 7
io.setmode(io.BOARD)
io.setup(pin_ir, io.IN) 

url = "http://localhost:5000/relais?status={}" # TODO config file

###############################################################################
def SendRelaisStatus (status):
    url_ = url.format(status)

    Log("SendRelaisStatus: {}".format(status))
    try:
        response = urllib.urlopen(url_)
        data = response.read().decode("utf-8")
    except (IOError):
        Log("Error: {0[0]} {0[1]}".format(sys.exc_info()))
        # raise ValueError
    except socket.timeout:
        Log("socket.timeout: {0[0]} {0[1]}".format(sys.exc_info()))
        # raise ValueError


###############################################################################
## main ######################################################################
last = None
while True:
    act = io.input(pin_ir)
    if act != last:
        if act == 1:
            SendRelaisStatus("off")
        else:
            SendRelaisStatus("on")

        last = act

    time.sleep(0.05)

# eof #

