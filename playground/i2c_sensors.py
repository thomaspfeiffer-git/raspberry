#!/usr/bin/python
# -*- coding: utf-8 -*-
###############################################################################
# i2c_sensors.py                                                              #
# (c) https://github.com/thomaspfeiffer-git 2016                              #
###############################################################################
"""Tests various i2c sensors"""


import sys
from time import sleep, strftime

sys.path.append('../libs')
sys.path.append('../libs/sensors')

import BMP180


bmp180 = BMP180.BMP180()

while True:
     print(strftime("%H:%M:%S"))
     print("Sensor | Größe | Messwert | Einheit |")
     print("BMP180 | Druck | %.1f     | hPa     |" % (bmp180.read_pressure()/100.0))
     print("BMP180 | Temp  | %.1f     | °C      |" % (bmp180.read_temperature()))
     print("")

     sleep(10)
