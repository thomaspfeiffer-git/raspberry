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

"""


"""
###### Usage ######
### Sensor
nohup ./Solarpower.py --sensor id 2>&1 > solar.log &

### Receiver
nohup ./Solarpower.py --receiver 2>&1 > solar.log &
"""


import argparse
import csv                         #### TODO to be removed later?
from datetime import datetime
import minimalmodbus
import os
import socket
import sys
import threading
import time


sys.path.append("../libs/")
from Logging import Log
from Shutdown import Shutdown
import UDP


CREDENTIALS = os.path.expanduser("~/credentials/solarpower.cred")
RRDFILE = os.path.expanduser("~/rrd/databases/solarpower.rrd")
UPDATE_INTERVAL = 50   # time delay between two measurements (seconds)


###############################################################################
###############################################################################
class Meter (object):
    def __init__ (self, usb_id, bus_id):
        self.__usb = usb_id
        self.__id = bus_id
        self.meter = minimalmodbus.Instrument(self.__usb, self.__id)
        self.meter.serial.baudrate = 9600

        self.values = {}
        for key in self.input_register:
            self.values[key] = 0

    def read (self):
        self.values[self.field_timestamp] = datetime.now().strftime("%Y%m%d %H:%M:%S")
        for key in self.input_register:
           try:
               value = self.meter.read_float(functioncode=4,
                                             registeraddress=self.input_register[key]["port"],
                                             number_of_registers=self.input_register[key]["digits"])
           except (minimalmodbus.InvalidResponseError, minimalmodbus.NoResponseError):
               pass
           else:
               self.values[key] = f"{value:.2f}"


###############################################################################
###############################################################################
class Main_Meter (Meter):
    field_timestamp = "Timestamp"
    field_V_L1 = "Voltage L1"
    field_V_L2 = "Voltage L2"
    field_V_L3 = "Voltage L3"
    field_I_L1 = "Current L1"
    field_I_L2 = "Current L2"
    field_I_L3 = "Current L3"
    field_I    = "Current total"
    field_P    = "Power"

    input_register = {
        field_V_L1: {
            "port": 0, "digits": 2, "Unit": "V"},
        field_V_L2: {
            "port": 2, "digits": 2, "Unit": "V"},
        field_V_L3: {
            "port": 4, "digits": 2, "Unit": "V"},
        field_I_L1: {
            "port": 6, "digits": 2, "Unit": "A"},
        field_I_L2: {
            "port": 8, "digits": 2, "Unit": "A"},
        field_I_L3: {
            "port": 10, "digits": 2, "Unit": "A"},
        field_I: {
            "port": 48, "digits": 2, "Unit": "A"},
        field_P: {
            "port": 52, "digits": 2, "Unit": "W"}
    }

    def __init__ (self, usb_id, bus_id):
        super().__init__(usb_id, bus_id)


###############################################################################
# Shutdown stuff ##############################################################
def shutdown_application ():
    """cleanup stuff"""
    Log("Stopping application")
    Log("Application stopped")
    sys.exit(0)


###############################################################################
## main #######################################################################
if __name__ == "__main__":
    shutdown_application = Shutdown(shutdown_func=shutdown_application)

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--sensor", help="read data from power meter and send to udp server", action="store_true")
    group.add_argument("--receiver", help="receive data via udp and store in rrd database", action="store_true")
    args = parser.parse_args()


    main_meter = Main_Meter('/dev/ttyUSB0', 1)
    # solar_meter = Solar_Meter('/dev/ttyUSB1', 2)


    csv_file = "solar.csv"
    csv_date = "Timestamp"
    csv_V_L1 = "Voltage L1"
    csv_V_L2 = "Voltage L2"
    csv_V_L3 = "Voltage L3"
    csv_I_L1 = "Current L1"
    csv_I_L2 = "Current L2"
    csv_I_L3 = "Current L3"
    csv_I    = "Current total"
    csv_P    = "Power"
    csv_fields = [csv_date, csv_V_L1, csv_V_L2, csv_V_L3, csv_I_L1, csv_I_L2, csv_I_L3, csv_I, csv_P]

    with open(csv_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames = csv_fields)
        writer.writeheader()

    while True:
        main_meter.read()
        with open(csv_file, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames = csv_fields)
            writer.writerow(main_meter.values)

        for _ in range(UPDATE_INTERVAL*10):  # interruptible sleep
            time.sleep(0.1)

# eof #

