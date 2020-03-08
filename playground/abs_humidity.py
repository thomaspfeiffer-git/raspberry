#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# abs_humidity.py                                                             #
# (c) https://github.com/thomaspfeiffer-git 2020                              #
###############################################################################
"""Calculates absolute humidity"""

import sys
import time

sys.path.append('../libs')

from Humidity import abs_humidity
from sensors.HTU21DF import HTU21DF
htu21df = HTU21DF()

while True:
     temperature = htu21df.read_temperature()
     humidity    = htu21df.read_humidity()
     abs_humi    = abs_humidity(humidity, temperature)

     print(f"Humi     | {humidity:>8.2f} | % rF  |")
     print(f"Temp     | {temperature:>8.2f} | °C    |")
     print(f"Abs Humi | {abs_humi:>8.2f} | g/m^3 |")

     time.sleep(1)

# eof #

