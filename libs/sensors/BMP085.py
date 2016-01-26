# -*- coding: utf-8 -*-
###############################################################################
# BMP085.py                                                                   #
# Communication with BMP085                                                   #
# (c) https://github.com/thomaspfeiffer-git 2016                              #
###############################################################################
"""provides a class for handling the air pressure sensor BMP085"""

import sys

import Adafruit_BMP085

# maybe necessary:
#     import numpy
#     for i in range(0,10):
#         p.append(sensor.readPressure())
#     p.sort()
#     p_avg = np.mean(p[int(len(p)/3):int(len(p)/3)*2])
# or check useability of class Measurements

class BMP085 (object):
    """class for handling the air pressure sensor BMP085"""
    def __init__ (self, qvalue=None):
        self.__bmp    = Adafruit_BMP085.BMP085(0x77, 2) 
        self.__qvalue = qvalue

    def read (self):
        """read sensor and return measured value"""
        value = self.__bmp.readPressure()

        if self.__qvalue is not None:
            self.__qvalue.value = "%.1f" % value/100.0

        return value

# eof #

