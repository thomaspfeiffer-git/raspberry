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
import csv                         #### TODO to be removed later?
from datetime import datetime
import os
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
# Meter #######################################################################
class Meter (object):
    def __init__ (self, usb_id, bus_id):
        import minimalmodbus
        self.valid_data = False

        self.__usb = usb_id
        self.__id = bus_id   ### TODO: check ID
        self.meter = minimalmodbus.Instrument(self.__usb, self.__id)
        self.meter.serial.baudrate = 9600

        self.values = {}
        for register in self.input_register:
            self.values[register] = 0

    def read (self):
        for register in self.input_register:
           try:
               value = self.meter.read_float(functioncode=4,
                                             registeraddress=self.input_register[register]["port"],
                                             number_of_registers=self.input_register[register]["digits"])
           except (minimalmodbus.InvalidResponseError, minimalmodbus.NoResponseError):
               pass
           else:
               self.values[register] = value
               self.valid_data = True

    def rrd (self):
        if self.valid_data:
            result = ""
            for i in self.fields:
                result += f"{self.values[i]:.2f}:"
            return result[:-1]
        else:
            pass ### TODO

    def rrd_template (self):
        result = ":"
        return (result.join(self.fields))


###############################################################################
# Main_Meter ##################################################################
class Main_Meter (Meter):
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

    input_register = {
        field_V_L1: { "port":   0, "digits": 2, "unit": "V" },
        field_V_L2: { "port":   2, "digits": 2, "unit": "V" },
        field_V_L3: { "port":   4, "digits": 2, "unit": "V" },
        field_I_L1: { "port":   6, "digits": 2, "unit": "A" },
        field_I_L2: { "port":   8, "digits": 2, "unit": "A" },
        field_I_L3: { "port":  10, "digits": 2, "unit": "A" },
        field_I_N:  { "port": 224, "digits": 2, "unit": "A" },
        field_I:    { "port":  48, "digits": 2, "unit": "A" },
        field_P:    { "port":  52, "digits": 2, "unit": "W" }
    }

    def __init__ (self, usb_id, bus_id):
        super().__init__(usb_id, bus_id)


###############################################################################
# Solar_Meter #################################################################
class Solar_Meter (Meter):
    field_V = "Solar_U"
    field_I = "Solar_I"
    field_P = "Solar_P"
    fields = [field_V, field_I, field_P]

    input_register = {
        field_V: { "port":  0, "digits": 2, "unit": "V" },
        field_I: { "port":  6, "digits": 2, "unit": "A" },
        field_P: { "port": 12, "digits": 2, "unit": "W" }
    }

    def __init__ (self, usb_id, bus_id):
        super().__init__(usb_id, bus_id)


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
                payload = f"{self.rrd_template}:N:{main_meter.rrd()}:{solar_meter.rrd()}"
                self.udp.send(payload)

    def stop (self):
        self._running = False


###############################################################################
# CSV #########################################################################
class CSV (object):
    def __init__ (self):
        self.csv_file = "solar.csv"
        self.csv_fields = ["Timestamp"] + Main_Meter.fields + Solar_Meter.fields

        with open(self.csv_file, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.csv_fields)
            writer.writeheader()

    def write (self):
        timestamp = datetime.now().strftime("%Y%m%d %H:%M:%S")
        values = main_meter.values | solar_meter.values
        for k in values.keys():
            values[k] = f"{values[k]:.2f}"

        with open(self.csv_file, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.csv_fields)
            writer.writerow({ "Timestamp": timestamp } | values)


###############################################################################
# Receiver ####################################################################
class Receiver (object):
    def __init__ (self):
        self.udp = UDP.Receiver(CREDENTIALS)

    def start (self):
        while True:
            payload = self.udp.receive()
            Log(f"RRD Data received: {payload}")




###############################################################################
# Shutdown stuff ##############################################################
def shutdown_application ():
    """cleanup stuff"""
    Log("Stopping application")
    if args.sensor is not None:
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
        r = Receiver()
        r.start()

    if args.sensor is not None:
        main_meter = Main_Meter('/dev/ttyUSB0', 1)
        solar_meter = Solar_Meter('/dev/ttyUSB1', 2)

        my_csv = CSV()

        storedata = StoreData()
        storedata.start()

        while True:
            main_meter.read()
            solar_meter.read()
            my_csv.write()

            for _ in range(UPDATE_INTERVAL*10):  # interruptible sleep
                time.sleep(0.1)

# eof #

