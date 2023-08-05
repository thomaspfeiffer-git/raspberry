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
# software

# https://minimalmodbus.readthedocs.io/en/stable/usage.html
sudo pip3 install -U minimalmodbus

"""

import time
import minimalmodbus

main_meter = minimalmodbus.Instrument('/dev/ttyUSB0', 1)
main_meter.serial.baudrate = 9600
# solar_meter = minimalmodbus.Instrument('/dev/ttyUSB1', 1)
# solar_meter.serial.baudrate = 9600

input_register = {
    "Spannung L1": {
        "port": 0, "digits": 2, "Unit": "V"},
    "Spannung L2": {
        "port": 2, "digits": 2, "Unit": "V"},
    "Spannung L3": {
        "port": 4, "digits": 2, "Unit": "V"},
    "Strom L1": {
        "port": 6, "digits": 2, "Unit": "A"},
    "Strom L2": {
        "port": 8, "digits": 2, "Unit": "A"},
    "Strom L3": {
        "port": 10, "digits": 2, "Unit": "A"},
    "aktueller Gesamtstrom": {
        "port": 48, "digits": 2, "Unit": "A"},
    "aktuelle Gesamtwirkleistung": {
        "port": 52, "digits": 2, "Unit": "W"}
}


main_meter_values = {}
for key in input_register:
    main_meter_values[key] = 0


for key in input_register:
    measurement = key
    try:
       value = main_meter.read_float(functioncode=4,
                                     registeraddress=input_register[key]["port"],
                                     number_of_registers=input_register[key]["digits"])
    except (minimalmodbus.InvalidResponseError, minimalmodbus.NoResponseError):
        value = "n/a"
    else:
        value = f"{value:.2f}"
    unit = input_register[key]["Unit"]

    print(f"{measurement}: {value} {unit}")
#    time.sleep(0.5)

# eof #

