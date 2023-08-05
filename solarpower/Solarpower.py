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

import csv
from datetime import datetime
import time
import minimalmodbus

main_meter = minimalmodbus.Instrument('/dev/ttyUSB0', 1)
main_meter.serial.baudrate = 9600
# solar_meter = minimalmodbus.Instrument('/dev/ttyUSB1', 1)
# solar_meter.serial.baudrate = 9600


csv_file = "solar.csv"
csv_V_L1 = "Voltage L1"
csv_V_L2 = "Voltage L2"
csv_V_L3 = "Voltage L3"
csv_I_L1 = "Current L1"
csv_I_L2 = "Current L2"
csv_I_L3 = "Current L3"
csv_I    = "Current total"
csv_P    = "Power"

input_register = {
    csv_V_L1: {
        "port": 0, "digits": 2, "Unit": "V"},
    csv_V_L2: {
        "port": 2, "digits": 2, "Unit": "V"},
    csv_V_L3: {
        "port": 4, "digits": 2, "Unit": "V"},
    csv_I_L1: {
        "port": 6, "digits": 2, "Unit": "A"},
    csv_I_L2: {
        "port": 8, "digits": 2, "Unit": "A"},
    csv_I_L3: {
        "port": 10, "digits": 2, "Unit": "A"},
    csv_I: {
        "port": 48, "digits": 2, "Unit": "A"},
    csv_P: {
        "port": 52, "digits": 2, "Unit": "W"}
}


csv_fields = ["Date", csv_V_L1, csv_V_L2, csv_V_L3, csv_I_L1, csv_I_L2, csv_I_L3, csv_I, csv_P]

with open(csv_file, 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames = csv_fields)
    writer.writeheader()


main_meter_values = {}
for key in input_register:
    main_meter_values[key] = 0

while True:
    for key in input_register:
        try:
           value = main_meter.read_float(functioncode=4,
                                         registeraddress=input_register[key]["port"],
                                         number_of_registers=input_register[key]["digits"])
        except (minimalmodbus.InvalidResponseError, minimalmodbus.NoResponseError):
            pass
        else:
            main_meter_values[key] = f"{value:.2f}"

    main_meter_values["Date"] = datetime.now().strftime("%Y%m%d %H:%M:%S")
    with open(csv_file, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames = csv_fields)
        writer.writerow(main_meter_values)

    for _ in range(500):  # interruptible sleep
        time.sleep(0.1)


# eof #

