#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
##############################################################################
# tests BME680                                                               #
# taken from https://github.com/pimoroni/bme680                              #
# (c) https://github.com/thomaspfeiffer-git 2017, 2018                       #
##############################################################################

import sys
import time

sys.path.append("../libs/")
from sensors.BME680 import BME680, BME_680_SECONDARYADDR

print("""Estimate indoor air quality

Runs the sensor for a burn-in period, then uses a 
combination of relative humidity and gas resistance
to estimate indoor air quality as a percentage.

Press Ctrl+C to exit

""")

sensor = BME680(i2c_addr=BME_680_SECONDARYADDR)

# start_time and curr_time ensure that the 
# burn_in_time (in seconds) is kept track of.

try:
    while True:
        sensor.get_sensor_data()
        print("{:.2f} °C; {:.2f} hPa; {:.2f} % rF; air quality: {:.2f}".format(sensor.data.temperature, sensor.data.pressure, sensor.data.humidity, sensor.data.air_quality_score))
        time.sleep(10)

except KeyboardInterrupt:
    pass
