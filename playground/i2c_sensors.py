#!/usr/bin/python
# -*- coding: utf-8 -*-
###############################################################################
# i2c_sensors.py                                                              #
# (c) https://github.com/thomaspfeiffer-git 2016                              #
###############################################################################
"""Tests various i2c sensors"""


import sys

sys.path.append('../libs')
sys.path.append('../libs/sensors')

import BMP085


bmp085 = BMP085.BMP085()   # todo: Lock; evtl als BMP180?


print "BMP180, Druck: %.1f hPa" % (bmp085.read()/100.0) 


