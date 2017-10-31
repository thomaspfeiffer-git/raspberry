#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys
import time

sys.path.append('../libs')
sys.path.append('../libs/sensors')

import BMP180


b = BMP180.BMP180()

while true:
    print "Druck: %s" % (b.read_pressure() / 100.0)
    print "Temp: %s" % b.read_temperature()
    time.sleep(60)


