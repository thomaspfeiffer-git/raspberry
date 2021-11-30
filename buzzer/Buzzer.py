#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# Buzzer.py                                                                   #
# (c) https://github.com/thomaspfeiffer-git 2021                              #
###############################################################################
""" """


### usage ###
# nohup ./Weatherstation.py 2>&1 >buzzer.log &


### useful ressources ###
# turn off screen saver:
# sudo apt-get install xscreensaver
# start xscreensaver and set screensaver off manually
#
# Packages you might install
# sudo apt-get install python3-pil.imagetk


import tkinter as tk
from tkinter.font import Font

import os
import sys
import time

sys.path.append('../libs')
from Shutdown import Shutdown
from Logging import Log


###############################################################################
# shutdown_application ########################################################
def shutdown_application ():
    """called on shutdown; stops all threads"""
    Log("Shutdown.")
    sys.exit(0)


###############################################################################
# Main ########################################################################
if __name__ == '__main__':
    try:
        os.environ["DISPLAY"]
    except KeyError:
        Log("$DISPLAY not set, using default :0.0")
        os.environ["DISPLAY"] = ":0.0"

    shutdown = Shutdown(shutdown_func=shutdown_application)


# eof #

