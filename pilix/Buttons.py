#!/usr/bin/python3 -u
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
from urllib.error import HTTPError, URLError 
from urllib.request import urlopen

sys.path.append("../libs/")
from Logging import Log

from config import CONFIG


io.setwarnings(False)
io.setmode(io.BOARD)
io.setup(CONFIG.PIN.BTN_Control, io.IN) 
io.setup(CONFIG.PIN.BTN_Battery, io.IN) 


url_shutdown = "shutdown"
url_toggle = "toggle"
url_battery = "battery?enabled={}"


###############################################################################
def CallPilixControl (param):
    Log("CallPilixControl: {}".format(param))
    try:
        with urlopen(CONFIG.API.url.format(param)) as response:
            data = response.read().decode("utf-8")
    except IOError:
        Log("Error: {0[0]} {0[1]}".format(sys.exc_info()))
    except socket.timeout:
        Log("socket.timeout: {0[0]} {0[1]}".format(sys.exc_info()))


###############################################################################
## main #######################################################################
time_pressed = None
time_released = None
last_btn_control = None
last_btn_battery = None

i = 0

while True:
    act_btn_control = io.input(CONFIG.PIN.BTN_Control)
    if act_btn_control != last_btn_control:
        if last_btn_control != None:
            if act_btn_control == 0:
                time_pressed = time.time()
            if act_btn_control == 1:
                time_released = time.time()
                if time_released - time_pressed > CONFIG.APP.delayToShutdown: 
                    CallPilixControl(url_shutdown)
                else:
                    CallPilixControl(url_toggle)
                time_pressed = None
                time_released = None
        last_btn_control = act_btn_control

    act_btn_battery = io.input(CONFIG.PIN.BTN_Battery)
    if act_btn_battery != last_btn_battery:
        CallPilixControl(url_battery.format(not bool(act_btn_battery)))
        last_btn_battery = act_btn_battery

    # resend state every 10 seconds.
    # just in case PilixControl was not running when switching the button.
    i += 1
    if i >= 200:
        CallPilixControl(url_battery.format(not bool(act_btn_battery)))
        i = 0

    time.sleep(0.05)

# eof #

