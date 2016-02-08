#!/usr/bin/python3
# -*- coding: utf-8 -*-
################################################################################
# PCF8591.py                                                                   #
# (c) https://github.com/thomaspfeiffer-git 2016                               #
################################################################################
"""controls A/D converter PCF8591"""

import sys
import time

sys.path.append('../libs')
sys.path.append('../libs/sensors')
from PCF8591 import PCF8591

if __name__ == '__main__':
    adc = PCF8591(0x48)

    while True:
        result = adc.read(channel=0)
        print("Result 0: %s" % result)
        result = adc.read(channel=1)
        print("Result 1: %s" % result)
        result = adc.read(channel=2)
        print("Result 2: %s" % result)
        result = adc.read(channel=3)
        print("Result 3: %s" % result)
        print("--------------------")
        time.sleep(0.5)

# eof #
 
