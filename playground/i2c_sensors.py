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

import BMP085


bmp085 = BMP085.BMP085()

while True:
     print(strftime("%H:%M:%S"))
     print("Sensor | Größe | Messwert | Einheit |")
     print("BMP180 | Druck | %.1f     | hPa     |" % (bmp085.read()/100.0) )
     print("")

     sleep(10)
