# -*- coding: utf-8 -*-
################################################################################
# pwm.py                                                                       #
# (c) https://github.com/thomaspfeiffer-git May 2016                           #
################################################################################
"""controls PWM output of Raspberry Pi"""

import wiringpi2 as wipi

class PWM (object):
    BRIGHT = 0    
    DARK   = 1023 

    def __init__ (self, pin=12):   # usually BCM GPIO 18
        self.__pin = pin
        wipi.wiringPiSetupPhys()
        wipi.pinMode(self.__pin, 2)

    def control (self, value):
        value = int(value)
        if (value > self.DARK):
            value = self.DARK
        if (value < self.BRIGHT):  
            value = self.BRIGHT
        print "PWM.control: %s" % value
        wipi.pwmWrite(self.__pin, value)

    def on (self):
        self.control(self.BRIGHT)

    def off (self):
        self.control(self.DARK)

# eof #
