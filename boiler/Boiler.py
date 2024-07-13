#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# Boiler.py                                                                   #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2024                   #
###############################################################################

"""
"""

### Usage ###
# nohup ./Boiler --duration 118 &
# nohup ./Boiler --start 14 --duration 118 &

### Packages you might need to install ###
# sudo apt install python3-gpiozero


import argparse
from datetime import datetime, timedelta
from gpiozero import Button, LED
import schedule
import sys
import time


sys.path.append("../libs/")
from Shutdown import Shutdown


###############################################################################
# CONFIG ######################################################################
class CONFIG:
    class Boiler:
        pin = "BOARD18"
    class Logging:
        file = "boiler.log"


###############################################################################
# MyLogging ###################################################################
class MyLogging (object):

    def __init__ (self):
        pass

    def __call__ (self, logstr):
        self.Log(logstr)

    def Log (self, logstr):
        import Logging

        Logging.Log(logstr)
        with open(CONFIG.Logging.file, mode='a') as logfile:
            Logging.Log(logstr, logfile)


###############################################################################
# Relais ######################################################################
class Relais (object):
    def __init__ (self, pin):
        self.__relais = LED(pin)

    def on (self):
        self.__relais.on()
        Log("Switched boiler on.")

    def off (self):
        self.__relais.off()
        Log("Switched boiler off.")


###############################################################################
# Shutdown stuff ##############################################################
def shutdown_application ():
    """cleanup stuff"""
    Log("Stopping application.")
    boiler.off()
    Log("Application stopped.")
    sys.exit(0)


###############################################################################
## main #######################################################################
if __name__ == "__main__":
    shutdown_application = Shutdown(shutdown_func=shutdown_application)
    Log = MyLogging()
    boiler = Relais(CONFIG.Boiler.pin)

    parser = argparse.ArgumentParser()
    parser.add_argument("--start", "-s", nargs=1, type=int,
                        help="Time of day (hour) the boiler shall be switched on.")
    parser.add_argument("--duration", "-d", nargs=1, type=int, default=[118],
                        help="Duration in minutes the boiler shall heat.")
    args = parser.parse_args()

    now = datetime.now()
    if args.start == None:
        start_time = now + timedelta(minutes=1)
    else:
        start_time = now.replace(hour=args.start[0], minute=1)
    if start_time < now:
        raise ValueError("Start time must be in the future.")

    stop_time = start_time + timedelta(minutes=args.duration[0])
    exit_time = stop_time + timedelta(minutes=1)

    start_time = f"{start_time.hour}:{start_time.minute:02d}"
    Log(f"Set start time to {start_time}.")
    stop_time = f"{stop_time.hour}:{stop_time.minute:02d}"
    Log(f"Set stop time to {stop_time}.")
    exit_time = f"{exit_time.hour}:{exit_time.minute:02d}"
    Log(f"Set exit time to {exit_time}.")

    schedule.every().day.at(start_time).do(boiler.on)
    schedule.every().day.at(stop_time).do(boiler.off)
    schedule.every().day.at(exit_time).do(lambda: shutdown_application.shutdown(0,0))

    while True:
        schedule.run_pending()
        time.sleep(1)

# eof #

