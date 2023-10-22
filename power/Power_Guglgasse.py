#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# Power_Guglgasse.py                                                          #
# (c) https://github.com/thomaspfeiffer-git 2023                              #
###############################################################################

"""
Measuring power consumption at home.
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
nohup ./Power_Guglgasse.py --sensor 2>&1 > solar.log &

### Receiver
nohup ./Power_Guglgasse.py --receiver 2>&1 > solar.log &
"""


import argparse
import csv
from datetime import datetime
import os
import sys
import threading
import time

sys.path.append("../libs/")
from Logging import Log
from Shutdown import Shutdown
import UDP

from Meters import SDM630


CREDENTIALS = os.path.expanduser("~/credentials/power_guglgasse.cred")
RRDFILE = os.path.expanduser("~/rrd/databases/power_guglgasse.rrd")
UPDATE_INTERVAL_READ_DATA       = 1   # time delay between two measurements (seconds)
UPDATE_INTERVAL_SEND_DATA_UDP   = 10  # interval for sending data to external server
UPDATE_INTERVAL_SEND_DATA_LOCAL = 1   # interval for sending data to internal server

BusID_Meter = 1


###############################################################################
# StoreData_UDP ###############################################################
class StoreData_UDP (threading.Thread):
    def __init__ (self):
        threading.Thread.__init__(self)

        self.udp = UDP.Sender(CREDENTIALS)
        self.rrd_template = f"{meter.rrd_template()}"

    def run (self):
        self._running = True
        while self._running:
            for _ in range(UPDATE_INTERVAL_SEND_DATA_UDP*10):
                if not self._running:
                    break
                time.sleep(0.1)

            if self._running:
                try:
                    payload = f"{self.rrd_template}:N:{meter.rrd()}"
                except RuntimeError:    # ignore empty data
                    pass
                else:
                    self.udp.send(payload)

    def stop (self):
        self._running = False


###############################################################################
# StoreData_Local #############################################################
class StoreData_Local (threading.Thread):
    def __init__ (self):
        threading.Thread.__init__(self)

    def run (self):
        self._running = True
        while self._running:
            for _ in range(UPDATE_INTERVAL_SEND_DATA_LOCAL*10):
                if not self._running:
                    break
                time.sleep(0.1)

            if self._running:
                try:
                    payload = f"{self.rrd_template}:N:{meter.rrd()}"
                except RuntimeError:    # ignore empty data
                    pass
                else:
                    pass
                    # TODO send data to local home automation project (pih)

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
# CSV #########################################################################
class CSV (object):
    def __init__ (self):
        self.fieldnames = ["Timestamp", SDM630.field_P]
        self.today = 0

        self.csv_directory = "csv/"

        if not os.path.isdir(self.csv_directory):
            os.makedirs(self.csv_directory)

        self.new_file()

    def new_file (self):
        if self.today != datetime.now().day:   # new day? --> start with new file
            self.today = datetime.now().day
            self.filename = f"{self.csv_directory}power_guglgasse_{datetime.now().strftime('%Y%m%d')}.csv"

            if not os.path.isfile(self.filename):
                with open(self.filename, 'w', newline='') as file:
                     writer = csv.DictWriter(file, fieldnames=self.fieldnames)
                     writer.writeheader()

    @staticmethod
    def get_item_from_rrd (rrd_template, rrd_data, item):
        return { item: rrd_data.split(':')[rrd_template.split(':').index(item)+1] }

    def write (self, rrd_template, rrd_data):
        self.new_file()
        csv_data = { "Timestamp": datetime.now().strftime("%Y%m%d %H:%M:%S") }
        csv_data.update(self.get_item_from_rrd(rrd_template, rrd_data, SDM630.field_P))

        with open(self.filename, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writerow(csv_data)


###############################################################################
# Shutdown stuff ##############################################################
def shutdown_application ():
    """cleanup stuff"""
    Log("Stopping application")
    if args.sensor:
        storedata_local.stop()
        storedata_local.join()
        storedata_udp.stop()
        storedata_udp.join()

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
        my_csv = CSV()
        r = Receiver()
        r.start()

    if args.sensor:
        meter = SDM630(BusID_Meter)

        storedata_udp = StoreData_UDP()
        storedata_udp.start()
        storedata_local = StoreData_Local()
        storedata_local.start()

        while True:
            meter.read()

            for _ in range(UPDATE_INTERVAL_READ_DATA*10):  # interruptible sleep
                time.sleep(0.1)

# eof #

