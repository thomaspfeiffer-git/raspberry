#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# Humidity.pyR                                                                #
# (c) https://github.com/thomaspfeiffer-git 2020                              #
###############################################################################
"""
Calculates absolute humidity
taken from https://www.kompf.de/weather/vent.html
"""

import math


# Compute saturated water vapor pressure in hPa
# Param t - temperature in °C
def svp(t):
  a = 6.112
  b = 17.67
  c = 243.5
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
def abs_humidity(rh, t):
  mw = 18.016 # kg/kmol (Molekulargewicht des Wasserdampfes)
  rs = 8314.3 # J/(kmol*K) (universelle Gaskonstante)
  ah = 10**5 * mw/rs * vp(rh, t)/(t + 273.15)
  return ah

# eof #

