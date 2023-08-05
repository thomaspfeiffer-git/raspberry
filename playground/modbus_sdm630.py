#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# modbus_sdm630.py                                                            #
# (c) https://github.com/thomaspfeiffer-git 2023                              #
###############################################################################

"""
prototyping usage of SDM630 via modbus

Sourcecode taken from
https://jojokorpi.ddns.net/wordpress/index.php/2021/06/01/sdm630-modbus-zaehler-auslesen/
"""


"""
# software

# https://minimalmodbus.readthedocs.io/en/stable/usage.html
sudo pip3 install -U minimalmodbus

"""

import time
import minimalmodbus

sdm630 = minimalmodbus.Instrument('/dev/ttyUSB0', 1)
sdm630.serial.baudrate = 9600

input_register = {
    "Spannung_L1": {
        "port": 0, "digits": 2, "Unit": "V"},
    "Spannung_L2": {
        "port": 2, "digits": 2, "Unit": "V"},
    "Spannung_L3": {
        "port": 4, "digits": 2, "Unit": "V"},
    "Strom_L1": {
        "port": 6, "digits": 2, "Unit": "A"},
    "Strom_L2": {
        "port": 8, "digits": 2, "Unit": "A"},
    "Strom_L3": {
        "port": 10, "digits": 2, "Unit": "A"},
    "aktueller_Gesamtstrom": {
        "port": 48, "digits": 2, "Unit": "A"},
    "aktuelle_Gesamtwirkleistung": {
        "port": 52, "digits": 2, "Unit": "W"}
}


for key in input_register:
    measurement = key
    value = sdm630.read_float(functioncode=4,
                              registeraddress=input_register[key]["port"],
                              number_of_registers=input_register[key]["digits"])
    unit = input_register[key]["Unit"]

    print(f"{measurement}: {value:.2f} {unit}")
    time.sleep(0.5)

# eof #

