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

     print(f"HTU21DF | Humi | {htu21df_humidity:>8.2f} | % rF |")
     print(f"HTU21DF | Temp | {htu21df_temperature:>8.2f} | °C   |")

     time.sleep(1)

# eof #

