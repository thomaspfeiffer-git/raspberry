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

from Adafruit import Adafruit_GPIO_Platform as Platform
platform = Platform.platform_detect()

import BME280    # air pressure, temperature, humidity
import DS1820    # temperature
import HTU21DF   # temperature, humidity
import CPU


bme280   = BME280.BME280()
ds1820_1 = DS1820.DS1820("/sys/bus/w1/devices/28-000006b50d05/w1_slave")
ds1820_2 = DS1820.DS1820("/sys/bus/w1/devices/28-000006b575fb/w1_slave")
ds1820_3 = DS1820.DS1820("/sys/bus/w1/devices/28-000006b58b12/w1_slave")
htu21df  = HTU21DF.HTU21DF()
cpu      = CPU.CPU()


while True:
     bme280_pressure     = bme280.read_pressure()/100.0
     bme280_temperature  = bme280.read_temperature()
     bme280_humidity     = bme280.read_humidity()
     if platform == Platform.BEAGLEBONE_BLACK: 
         ds1820_1.consume_cpu_start()
     ds1820_1_temperature = ds1820_1.read_temperature()
     ds1820_2_temperature = ds1820_2.read_temperature()
     ds1820_3_temperature = ds1820_3.read_temperature()
     if platform == Platform.BEAGLEBONE_BLACK: 
         ds1820_1.consume_cpu_stop()
     htu21df_temperature = htu21df.read_temperature()
     htu21df_humidity    = htu21df.read_humidity()
     cpu_temp            = cpu.read_temperature()
     
     values = ":".join("{:.2f}".format(d) for d in [bme280_pressure,      \
                                                    bme280_humidity,      \
                                                    htu21df_humidity,     \
                                                    bme280_temperature,   \
                                                    htu21df_temperature,  \
                                                    ds1820_1_temperature, \
                                                    ds1820_2_temperature, \
                                                    ds1820_3_temperature, \
                                                    cpu_temp])
     print(strftime("%Y%m%d %X:"), values)

     sleep(60)

# eof #

