#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sys
import time

sys.path.append('../libs')
sys.path.append('../libs/sensors')

import BMP180


b = BMP180.BMP180()

while True:
    print("Druck: {}".format(b.read_pressure() / 100.0))
    print("Temp: {}".format(b.read_temperature()))
    time.sleep(60)


