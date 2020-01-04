#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# bme280_test.py                                                              #
# (c) https://github.com/thomaspfeiffer-git 2016, 2020                        #
###############################################################################
"""Tests sensor BME280 (air pressure, humidity, temperature."""

import sys
import time

sys.path.append('../libs')

from sensors.BME280 import BME280    # air pressure, temperature, humidity

bme280 = BME280()

while True:
     bme280_pressure    = bme280.read_pressure()/100.0
     bme280_temperature = bme280.read_temperature()
     bme280_humidity    = bme280.read_humidity()

     print(f"BME280 | Press | {bme280_pressure:>8.2f} | hPa  |")
     print(f"BME280 | Humi  | {bme280_humidity:>8.2f} | % rF |")
     print(f"BME280 | Temp  | {bme280_temperature:>8.2f} | °C   |")

     time.sleep(1)

# eof #

