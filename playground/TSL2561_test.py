#!/usr/bin/python3
# -*- coding: utf-8 -*-
###############################################################################
# (c) https://github.com/thomaspfeiffer-git 2016, 2017                        #
###############################################################################

import sys
from time import sleep, strftime


sys.path.append('../libs')
sys.path.append('../libs/sensors')

from Adafruit import Adafruit_GPIO_Platform as Platform
platform = Platform.platform_detect()

import TSL2561   # luminosity

tsl2561   = TSL2561.TSL2561()

while True:
     tsl2561_luminosity  = tsl2561.lux()
     print("TLS2561    | Hell  | {:>8.2f} | C       |".format(tsl2561_luminosity))
     sleep(1)

