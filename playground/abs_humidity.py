#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# abs_humidity.py                                                             #
# (c) https://github.com/thomaspfeiffer-git 2020                              #
###############################################################################
"""Calculates absolute humidity"""

import math
import sys
import time

sys.path.append('../libs')


from sensors.HTU21DF import HTU21DF
htu21df = HTU21DF()


# taken from https://www.kompf.de/weather/vent.html
a = 6.112
b = 17.67
c = 243.5


# Compute saturated water vapor pressure in hPa
# Param t - temperature in °C
def svp(t):
  svp = a * math.exp((b*t)/(c+t))
  return svp


# Compute actual water vapor pressure in hPa
# Param rh - relative humidity in %
# Param t - temperature in °C
def vp(rh, t):
  vp = rh/100. * svp(t)
  return vp


# Compute the absolute humidity in g/m³
# Param rh - relative humidity in %
# Param t - temperature in °C
def ah(rh, t):
  mw = 18.016 # kg/kmol (Molekulargewicht des Wasserdampfes)
  rs = 8314.3 # J/(kmol*K) (universelle Gaskonstante)
  ah = 10**5 * mw/rs * vp(rh, t)/(t + 273.15)
  return ah



while True:
     temperature = htu21df.read_temperature()
     humidity    = htu21df.read_humidity()
     abs_humi    = ah(humidity, temperature)

     print(f"Humi     | {humidity:>8.2f} | % rF   |")
     print(f"Temp     | {temperature:>8.2f} | °C  |")
     print(f"Abs Humi | {abs_humi:>8.2f} | g/m^3 |")

     time.sleep(1)

# eof #

