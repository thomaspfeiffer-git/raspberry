#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
#############################################################################



import sys
from time import sleep


sys.path.append("../libs/")
from i2c import I2C
from actuators.PCA9685 import PCA9685, PCA9685_BASE_ADDRESS



###############################################################################
# PWM #########################################################################
class PWM (PCA9685):
    def __init__ (self, channel):
        super().__init__(address=PCA9685_BASE_ADDRESS)
        self.__channel = channel

    def set_pwm_l (self, on):
        super().set_pwm(self.__channel, self.MAX-int(on), self.MAX)

# eof #



pwm = PWM(0)

while True:
    i = PWM.MIN
    while i < PWM.MAX:
        i = i + 10
        pwm.set_pwm_l(i)

    while i > PWM.MIN:
        i = i - 10
        pwm.set_pwm_l(i)

# eof #

