#!/usr/bin/python -u
# -*- coding: utf-8 -*-
###############################################################################
# Buttons.py                                                                  #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2017                   #
###############################################################################
"""controls the buttons:
   - button 1: toggle camera on/off and shutdown
   - button 2: using battery or main power supply (switch)"""
   

### usage ###
# nohup sudo ./Buttons.py > buttons.log 2>&1 &


import RPi.GPIO as io
import socket
import sys
import time
import urllib

sys.path.append("../libs/")
from Logging import Log


pin = 21    # TODO: config file
io.setmode(io.BOARD)
io.setup(pin, io.IN) 

url = "http://localhost:5000/{}" # TODO config file
url_shutdown = "shutdown"
url_toggle = "toggle"
time_delay_to_reset = 3.0 # TODO: config file


###############################################################################
def CallFelixControl (param):
    Log("CallFelixControl: {}".format(param))
    try:
        response = urllib.urlopen(url.format(param))
        data = response.read().decode("utf-8")
    except IOError:
        Log("Error: {0[0]} {0[1]}".format(sys.exc_info()))
    except socket.timeout:
        Log("socket.timeout: {0[0]} {0[1]}".format(sys.exc_info()))


###############################################################################
## main #######################################################################
time_pressed = None
time_released = None
last = None

while True:
    act = io.input(pin)
    if act != last:
        if last != None:
            if act == 0:
                time_pressed = time.time()
            if act == 1:
                time_released = time.time()
                if time_released - time_pressed > time_delay_to_reset:
                    CallFelixControl(url_shutdown)
                else:
                    CallFelixControl(url_toggle)
                time_pressed = None
                time_released = None
        last = act

    time.sleep(0.05)

# eof #

