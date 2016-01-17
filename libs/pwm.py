# -*- coding: utf-8 -*-
################################################################################
# pwm.py                                                                       #
# (c) https://github.com/thomaspfeiffer-git May 2016                           #
################################################################################
"""controls PWM output of Raspberry Pi"""

import wiringpi2 as wipi

class PWM (object):
    MAX = 1023    # bright
    MIN = 0       # dark

    def __init__ (self, pin=12):   # usually BCM GPIO 18
        self.__pin = pin
        wipi.wiringPiSetupPhys()
        wipi.pinMode(self.__pin, 2)

    def control (self, value):
        value = int(value)
        if (value > self.MAX):
            value = self.MAX
        if (value < self.MIN):  
            value = self.MIN
        wipi.pwmWrite(self.__pin, value)

    def on (self):
        self.control(self.MAX)

    def off (self):
        self.control(self.MIN)

# eof #
