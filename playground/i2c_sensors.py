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
     bmp180_pressure    = bmp180.read_pressure()/100.0
     bmp180_temperature = bmp180.read_temperature()
     bme280_pressure    = bme280.read_pressure()/100.0
     bme280_temperature = bme280.read_temperature()
     bme280_humidity    = bme280.read_humidity()
     mcp9808_1_temp     = mcp9808_1.read_temperature()
     mcp9808_2_temp     = mcp9808_2.read_temperature()
      
     print("{}: {}".format(strftime("%H:%M:%S")), ":".join((bmp180_pressure, bmp180_temperature, bme280_pressure, bme280_temperature, bme280_humidity, mcp9808_1_temp, mcp9808_2_temp))
     print("Sensor     | Größe | Messwert | Einheit |")
     print("BMP180     | Druck | {:>8.2f} | hPa     |".format(bmp180_pressure))
     print("BMP180     | Temp  | {:>8.2f} | °C      |".format(bmp180_temperature))
     print("BME280     | Druck | {:>8.2f} | hPa     |".format(bme280_pressure))
     print("BME280     | Temp  | {:>8.2f} | °C      |".format(bme280_temperature))
     print("BME280     | Humi  | {:>8.2f} | % rF    |".format(bme280_humidity))
     print("MCP9808 #1 | Temp  | {:>8.2f} | °C      |".format(mcp9808_1_temp))
     print("MCP9808 #2 | Temp  | {:>8.2f} | °C      |".format(mcp9808_2_temp))
     print("")

     sleep(10)


# eof #

