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
import csv
from datetime import datetime
import os
import serial
import sys
import threading
import time

sys.path.append("../libs/")
from Logging import Log
from Shutdown import Shutdown
import UDP


CREDENTIALS = os.path.expanduser("~/credentials/solarpower.cred")
RRDFILE = os.path.expanduser("~/rrd/databases/solar.rrd")
UPDATE_INTERVAL = 10   # time delay between two measurements (seconds)

BusID_MainMeter = 1
BusID_SolarMeter = 2


###############################################################################
# Meter #######################################################################
class Meter (object):
    def __init__ (self, bus_id):
        self.valid_data = False

        self.__id = bus_id
        self.meter = self.find_meter()

        self.values = {}
        for register in self.input_register:
            self.values[register] = 0

    def find_meter (self):
        for usb_node in [ f"/dev/ttyUSB{i}" for i in range(4) ]:
            Log(f"Searching meter with ID #{self.__id} on {usb_node} ...")
            try:
                meter = minimalmodbus.Instrument(usb_node, self.__id)
                meter.serial.baudrate = 9600
                meter.read_float(functioncode=4, registeraddress=0, number_of_registers=2)
            except (FileNotFoundError, serial.serialutil.SerialException, minimalmodbus.NoResponseError):
                Log(f"No meter with ID #{self.__id} found on {usb_node}.")
            else:
                Log(f"Found meter with ID #{self.__id} on {usb_node}.")
                return meter

        Log(f"No meter with ID {self.__id} found.")
        sys.exit(1)

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
            Log(f"No valid data from sensor #{self.__id} yet.")
            raise RuntimeError(f"No valid data from sensor #{self.__id} yet.")

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

    def __init__ (self, bus_id):
        super().__init__(bus_id)


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

    def __init__ (self, bus_id):
        super().__init__(bus_id)


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
# CSV #########################################################################
class CSV (object):
    def __init__ (self):
        self.fieldnames = ["Timestamp", Main_Meter.field_P, Solar_Meter.field_P]
        self.today = 0
        self.new_file()

    def new_file (self):
        if self.today != datetime.now().day:   # new day? --> start with new file
            self.today = datetime.now().day
            self.filename = f"csv/solarpower_{datetime.now().strftime('%Y%m%d')}.csv"

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
        csv_data.update(self.get_item_from_rrd(rrd_template, rrd_data, Main_Meter.field_P))
        csv_data.update(self.get_item_from_rrd(rrd_template, rrd_data, Solar_Meter.field_P))

        with open(self.filename, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writerow(csv_data)


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
        my_csv = CSV()
        r = Receiver()
        r.start()

    if args.sensor:
        import minimalmodbus
        main_meter = Main_Meter(BusID_MainMeter)
        solar_meter = Solar_Meter(BusID_SolarMeter)

        storedata = StoreData()
        storedata.start()

        while True:
            main_meter.read()
            solar_meter.read()

            for _ in range(UPDATE_INTERVAL*10):  # interruptible sleep
                time.sleep(0.1)

# eof #

