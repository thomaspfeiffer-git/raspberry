#!/usr/bin/python3
# -*- coding: utf-8 -*-
###############################################################################
# test_htu21df.py                                                             #
# (c) https://github.com/thomaspfeiffer-git 2016                              #
###############################################################################
"""Tests sensor HTU21DF (humidity, temperature."""


import sys
from time import sleep, strftime

sys.path.append('../libs')
sys.path.append('../libs/sensors')

import HTU21DF   # temperature, humidity

htu21df = HTU21DF.HTU21DF()

while True:
     htu21df_temperature = htu21df.read_temperature()
     htu21df_humidity    = htu21df.read_humidity()

     values = ":".join("{:.2f}".format(d) for d in [htu21df_humidity,    \
                                                    htu21df_temperature])
     print(strftime("%X:"), values)
     # print("HTU21DF    | Humi  | {:>8.2f} | % rF    |".format(htu21df_humidity))
     # print("HTU21DF    | Temp  | {:>8.2f} | C       |".format(htu21df_temperature))

     sleep(1)

# eof #

