#!/usr/bin/python -u
# -*- coding: utf-8 -*-
############################################################################
# Button.py                                                                #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2017                #
############################################################################
"""control lighting of our anteroom:
   check button and toggle anteroom's light on and off"""

### usage ###
# sudo Button.py

import RPi.GPIO as io
import socket
import sys
import time
import urllib

sys.path.append("../libs/")
from Logging import Log


pin_ir = 8
io.setmode(io.BOARD)
io.setup(pin_ir, io.IN) 

url = "http://localhost:5000/toggle" # TODO config file


###############################################################################
def CallToggle ():
    try:
        response = urllib.urlopen(url)
        data = response.read().decode("utf-8")
        Log("toggled!")
    except (IOError):
        Log("Error: {0[0]} {0[1]}".format(sys.exc_info()))
        raise ValueError
    except socket.timeout:
        Log("socket.timeout: {0[0]} {0[1]}".format(sys.exc_info()))
        raise ValueError


###############################################################################
## main ######################################################################
last = None
while True:
    act = io.input(pin_ir)   # TODO: debounce if necessary
    if act != last:
        if last == 1 and act == 0:  # falling edge
            CallToggle()
        last = act

    time.sleep(0.05)

# eof #

