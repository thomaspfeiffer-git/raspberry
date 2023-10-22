#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# Solarpower.py                                                               #
# (c) https://github.com/thomaspfeiffer-git 2023                              #
###############################################################################

"""
Measuring local photovoltaics.
"""


"""
### Libraries you might need to install:
# https://minimalmodbus.readthedocs.io/en/stable/usage.html
sudo pip3 install -U minimalmodbus


### Useful documentation:
# Registers of power meters:
# https://github.com/belba/SDMxxx/blob/master/sdm.py#L76

"""


"""
###### Usage ######
### Sensor
nohup ./Solarpower.py --sensor 2>&1 > solar.log &

### Receiver
nohup ./Solarpower.py --receiver 2>&1 > solar.log &
"""


import argparse
import os
import sys
import threading
import time

sys.path.append("../libs/")
from Logging import Log
from Shutdown import Shutdown
import UDP

from CSV import CSV
from Meters import SDM630, SDM230


CREDENTIALS = os.path.expanduser("~/credentials/solarpower.cred")
RRDFILE = os.path.expanduser("~/rrd/databases/solar.rrd")
UPDATE_INTERVAL = 10   # time delay between two measurements (seconds)

BusID_MainMeter = 1
BusID_SolarMeter = 2


###############################################################################
# StoreData ###################################################################
class StoreData (threading.Thread):
    def __init__ (self):
        threading.Thread.__init__(self)

        self.udp = UDP.Sender(CREDENTIALS)
        self.rrd_template = f"{main_meter.rrd_template()}:{solar_meter.rrd_template()}"

    def run (self):
        self._running = True
        while self._running:
            for _ in range(UPDATE_INTERVAL*10):
                if not self._running:
                    break
                time.sleep(0.1)

            if self._running:
                try:
                    payload = f"{self.rrd_template}:N:{main_meter.rrd()}:{solar_meter.rrd()}"
                except RuntimeError:    # ignore empty data
                    pass
                else:
                    self.udp.send(payload)

    def stop (self):
        self._running = False


###############################################################################
# Receiver ####################################################################
class Receiver (object):
    def __init__ (self):
        self.udp = UDP.Receiver(CREDENTIALS)

    def start (self):
        while True:
            payload = self.udp.receive()
            try:
                rrd_template = payload.split(":N:")[0]
                rrd_data = "N:" + payload.split(":N:")[1]
            except IndexError:
                Log("Wrong data format: {0[0]} {0[1]}".format(sys.exc_info()))
            else:
                my_csv.write(rrd_template, rrd_data)
                try:
                    import rrdtool
                    rrdtool.update(RRDFILE, "--template", rrd_template, rrd_data)
                except rrdtool.OperationalError:
                    Log("Cannot update rrd database: {0[0]} {0[1]}".format(sys.exc_info()))


###############################################################################
# Shutdown stuff ##############################################################
def shutdown_application ():
    """cleanup stuff"""
    Log("Stopping application")
    if args.sensor:
        storedata.stop()
        storedata.join()

    Log("Application stopped")
    sys.exit(0)


###############################################################################
## main #######################################################################
if __name__ == "__main__":
    shutdown_application = Shutdown(shutdown_func=shutdown_application)

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--sensor", help="read data from power meters and send to udp server", action="store_true")
    group.add_argument("--receiver", help="receive data via udp and store in rrd database", action="store_true")
    args = parser.parse_args()

    if args.receiver:
        my_csv = CSV("solarpower", [SDM630.field_P, SDM230.field_P])
        r = Receiver()
        r.start()

    if args.sensor:
        main_meter = SDM630(BusID_MainMeter)
        solar_meter = SDM230(BusID_SolarMeter)

        storedata = StoreData()
        storedata.start()

        while True:
            main_meter.read()
            solar_meter.read()

            for _ in range(UPDATE_INTERVAL*10):  # interruptible sleep
                time.sleep(0.1)

# eof #

