# -*- coding: utf-8 -*-
###############################################################################
# Meters.py                                                                   #
# (c) https://github.com/thomaspfeiffer-git 2023                              #
###############################################################################

"""
Library for using power meters SDM230 and SDM630.
"""


"""
### Libraries you might need to install:
# https://minimalmodbus.readthedocs.io/en/stable/usage.html
sudo pip3 install -U minimalmodbus


### Useful documentation:
# Registers of power meters:
# https://github.com/belba/SDMxxx/blob/master/sdm.py#L76

"""


import minimalmodbus
import serial
import sys

sys.path.append("../libs/")
from Logging import Log


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
# SDM630 ######################################################################
class SDM630 (Meter):
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
# SDM230 ######################################################################
class SDM230 (Meter):
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

# eof #

