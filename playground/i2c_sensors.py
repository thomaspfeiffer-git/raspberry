#!/usr/bin/python3
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

import BME280    # air pressure, temperature, humidity
import BMP180    # air pressure, temperature
import MCP9808   # temperatur

bmp180  = BMP180.BMP180()
bme280  = BME280.BME280()


MCP9808_1_ADDR = 0x18
MCP9808_2_ADDR = 0x19
mcp9808_1 = MCP9808.MCP9808(address=MCP9808_1_ADDR)
mcp9808_2 = MCP9808.MCP9808(address=MCP9808_2_ADDR)


while True:
     print(strftime("%H:%M:%S"))
     print("Sensor     | Größe | Messwert | Einheit |")
     print("BMP180     | Druck | {:>8.2f} | hPa     |".format(bmp180.read_pressure()/100.0))
     print("BMP180     | Temp  | {:>8.2f} | °C      |".format(bmp180.read_temperature()))
     print("BME280     | Druck | {:>8.2f} | hPa     |".format(bme280.read_pressure()/100.0))
     print("BME280     | Temp  | {:>8.2f} | °C      |".format(bme280.read_temperature()))
     print("BME280     | Humi  | {:>8.2f} | % rF    |".format(bme280.read_humidity()))
     print("MCP9808 #1 | Temp  | {:>8.2f} | °C      |".format(mcp9808_1.read_temperature()))
     print("MCP9808 #2 | Temp  | {:>8.2f} | °C      |".format(mcp9808_2.read_temperature()))
     print("")

     sleep(10)


# eof #

