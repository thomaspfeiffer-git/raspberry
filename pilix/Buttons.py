#!/usr/bin/python -u
# -*- coding: utf-8 -*-
###############################################################################
# Buttons.py                                                                  #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2017                   #
###############################################################################
"""controls the buttons:
   - button 1: toggle camera on/off and shutdown
   - button 2: using battery or main power supply (switch)"""


# FriendlyArm's gpio lib works with python 2.x only.
   

### usage ###
# nohup sudo ./Buttons.py > ./Logs/buttons.log 2>&1 &


import RPi.GPIO as io
import socket
import sys
import time
import urllib

sys.path.append("../libs/")
from Logging import Log

from config import CONFIG


pin = CONFIG.PIN.BTN_Control
io.setmode(io.BOARD)
io.setup(pin, io.IN) 

url = CONFIG.API.url
url_shutdown = "shutdown"
url_toggle = "toggle"
delay_to_shutdown = CONFIG.APP.delayToShutdown


###############################################################################
def CallPilixControl (param):
    Log("CallPilixControl: {}".format(param))
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
                if time_released - time_pressed > delay_to_shutdown:
                    CallPilixControl(url_shutdown)
                else:
                    CallPilixControl(url_toggle)
                time_pressed = None
                time_released = None
        last = act

    time.sleep(0.05)

# eof #

