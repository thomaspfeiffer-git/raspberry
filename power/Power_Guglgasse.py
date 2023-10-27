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
import os
import sys
import threading
import time

sys.path.append("../libs/")
from Logging import Log
from Shutdown import Shutdown
import UDP

from CSV import CSV
from Meters import SDM630


CREDENTIALS_RRD = os.path.expanduser("~/credentials/power_guglgasse.cred")
CREDENTIALS_UDP_HOMEAUTOMATION = os.path.expanduser("~/credentials/homeautomation.cred")
RRDFILE = os.path.expanduser("~/rrd/databases/power_guglgasse.rrd")

UPDATE_INTERVAL_READ_DATA = 1                 # time delay between two measurements (seconds)
UPDATE_INTERVAL_SEND_DATA_UDP = 10            # interval for sending data to external server
UPDATE_INTERVAL_SEND_DATA_HOMEAUTOMATION = 1  # interval for sending data to homeautomation server

BusID_Meter = 1



###############################################################################
###############################################################################
class Fake_SDM630 (object):
    field_V_L1 = "Main_U_L1"
    field_V_L2 = "Main_U_L2"
    field_V_L3 = "Main_U_L3"
    field_I_L1 = "Main_I_L1"
    field_I_L2 = "Main_I_L2"
    field_I_L3 = "Main_I_L3"
    field_I_N  = "Main_I_N"
    field_I    = "Main_I_tot"
    field_P    = "Main_P"
    fields = [field_V_L1, field_V_L2, field_V_L3,
              field_I_L1, field_I_L2, field_I_L3, field_I_N, field_I, field_P]

    def __init__ (self):
        self.valid_data = False
        self.values = {}
        for register in self.fields:
            self.values[register] = 0

    def read (self):
        import random
        import datetime
        self.values[self.field_V_L1] = 200.0 + random.randint(0,50)
        self.values[self.field_V_L2] = 300.0 + random.randint(0,50)
        self.values[self.field_V_L3] = 400.0 + random.randint(0,50)
        self.values[self.field_I_L1] = 1.0
        self.values[self.field_I_L2] = 2.0
        self.values[self.field_I_L3] = 3.0
        self.values[self.field_I_N]  = 4.0
        self.values[self.field_I]    = 9.0
        self.values[self.field_P]    = datetime.datetime.now().hour * 200 + datetime.datetime.now().minute
        self.valid_data = True

    def rrd (self):
        if self.valid_data:
            result = ""
            for i in self.fields:
                result += f"{self.values[i]:.2f}:"
            return result[:-1]
        else:
            Log(f"No valid data from sensor #{self.__id} yet.")
            raise RuntimeError(f"No valid data from sensor #{self.__id} yet.")

    def rrd_template (self):
        result = ":"
        return (result.join(self.fields))


###############################################################################
# StoreData_RRD ###############################################################
class StoreData_RRD (threading.Thread):
    def __init__ (self):
        threading.Thread.__init__(self)

        self.udp = UDP.Sender(CREDENTIALS_RRD)
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
# StoreData_Homeautomation ####################################################
class StoreData_Homeautomation (threading.Thread):
    def __init__ (self):
        threading.Thread.__init__(self)

        self.udp = UDP.Sender(CREDENTIALS_UDP_HOMEAUTOMATION)
        self.rrd_template = f"{meter.rrd_template()}"

    def run (self):
        self._running = True
        while self._running:
            for _ in range(UPDATE_INTERVAL_SEND_DATA_HOMEAUTOMATION*10):
                if not self._running:
                    break
                time.sleep(0.1)

            if self._running:
                try:
                    payload = f"Power - {self.rrd_template}:N:{meter.rrd()}"
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
        self.udp = UDP.Receiver(CREDENTIALS_RRD)

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
        storedata_homeautomation.stop()
        storedata_homeautomation.join()
        storedata_rrd.stop()
        storedata_rrd.join()

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
        my_csv = CSV("power_guglgasse", [SDM630.field_P])
        r = Receiver()
        r.start()

    if args.sensor:
        # meter = SDM630(BusID_Meter)
        meter = Fake_SDM630()

        storedata_rrd = StoreData_RRD()
        storedata_rrd.start()
        storedata_homeautomation = StoreData_Homeautomation()
        storedata_homeautomation.start()

        while True:
            meter.read()

            for _ in range(UPDATE_INTERVAL_READ_DATA*10):  # interruptible sleep
                time.sleep(0.1)

# eof #

