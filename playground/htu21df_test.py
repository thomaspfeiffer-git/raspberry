#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# test_htu21df.py                                                             #
# (c) https://github.com/thomaspfeiffer-git 2016, 2020                        #
###############################################################################
"""Tests sensor HTU21DF (humidity, temperature)."""


import sys
import time

sys.path.append('../libs')

from sensors.HTU21DF import HTU21DF  # temperature, humidity

htu21df = HTU21DF()

while True:
     htu21df_temperature = htu21df.read_temperature()
     htu21df_humidity    = htu21df.read_humidity()

     print("HTU21DF | Humi | {:>8.2f} | % rF |".format(htu21df_humidity))
     print("HTU21DF | Temp | {:>8.2f} | °C   |".format(htu21df_temperature))

     time.sleep(1)

# eof #

