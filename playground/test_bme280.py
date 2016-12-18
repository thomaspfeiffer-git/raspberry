#!/usr/bin/python3
# -*- coding: utf-8 -*-
###############################################################################
# test_bme280.py                                                              #
# (c) https://github.com/thomaspfeiffer-git 2016                              #
###############################################################################
"""Tests sensor BME280 (air pressure, humidity, temperature."""


import sys
from time import sleep, strftime

sys.path.append('../libs')
sys.path.append('../libs/sensors')

import BME280    # air pressure, temperature, humidity

bme280  = BME280.BME280()

while True:
     bme280_pressure     = bme280.read_pressure()/100.0
     bme280_temperature  = bme280.read_temperature()
     bme280_humidity     = bme280.read_humidity()

     print("BME280     | Druck | {:>8.2f} | hPa     |".format(bme280_pressure))
     print("BME280     | Humi  | {:>8.2f} | % rF    |".format(bme280_humidity))
     print("BME280     | Temp  | {:>8.2f} | C       |".format(bme280_temperature))

     sleep(1)

# eof #

