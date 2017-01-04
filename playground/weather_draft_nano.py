#!/usr/bin/python3
# -*- coding: utf-8 -*-
###############################################################################
# weather_draft_nano.py                                                       #
# (c) https://github.com/thomaspfeiffer-git 2016                              #
###############################################################################
"""Prepares a new weather.py running on a NanoPi NEO Air"""
"""(runs on a Raspberry Pi as well :-) )"""


import sys
from time import sleep, strftime

sys.path.append('../libs')
sys.path.append('../libs/sensors')

import BME280    # air pressure, temperature, humidity
import DS1820    # temperature
import HTU21DF   # temperature, humidity
import CPU

bme280  = BME280.BME280()
ds1820  = DS1820.DS1820("/sys/bus/w1/devices/28-000006b50d05/w1_slave")
htu21df = HTU21DF.HTU21DF()
cpu     = CPU.CPU()


while True:
     bme280_pressure     = bme280.read_pressure()/100.0
     bme280_temperature  = bme280.read_temperature()
     bme280_humidity     = bme280.read_humidity()
     ds1820_temperature  = ds1820.read()
     htu21df_temperature = htu21df.read_temperature()
     htu21df_humidity    = htu21df.read_humidity()
     cpu_temp            = cpu.read_temperature()
     
     values = ":".join("{:.2f}".format(d) for d in [bme280_pressure,     \
                                                    bme280_humidity,     \
                                                    htu21df_humidity,    \
                                                    bme280_temperature,  \
                                                    htu21df_temperature, \
                                                    ds1820_temperature,  \
                                                    cpu_temp])
     print(strftime("%Y%m%d %X:"), values)

     sleep(60)

# eof #

