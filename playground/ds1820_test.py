#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# ds1820_test.py                                                              #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2025                   #
###############################################################################

"""
Test application for temperature sensor DS1820.
"""

### Usage ###
# ./ds1820_test.py sensor id
# ./ds1820_test.py 28-030297946b71


import argparse
import sys
import time

sys.path.append('../libs')

from Logging import Log
from sensors.DS1820 import DS1820

parser = argparse.ArgumentParser()
parser.add_argument("sensor id")
ID = vars(parser.parse_args())['sensor id']

Log(f"Reading temperature from sensor {ID}.")
ds1820 = DS1820(f"/sys/bus/w1/devices/{ID}/w1_slave")

while True:
    Log(f"{ds1820.read_temperature()} C")
    for _ in range(100):  # interruptible sleep
        time.sleep(0.01)

# eof #

