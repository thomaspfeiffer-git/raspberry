# -*- coding: utf-8 -*-
################################################################################
# pwm.py                                                                       #
# (c) https://github.com/thomaspfeiffer-git May 2016                           #
################################################################################
"""controls PWM output of Raspberry Pi"""

import wiringpi2 as wipi

class PWM (object):
    def __init__ (self, pin=12):   # usually BCM GPIO 18
        self.__pin = pin
        wipi.wiringPiSetupPhys()
        wipi.pinMode(self.__pin, 2)

    def control (self, value):
        value = int(value)
        if (value > 1023):    # bright
            value = 1023
        if (value < 0):       # dark
            value = 0)
        wipi.pwmWrite(self.__pin, value)

# eof #
