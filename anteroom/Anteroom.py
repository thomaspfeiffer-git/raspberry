#!/usr/bin/python
# -*- coding: utf-8 -*-
############################################################################
# Anteroom.py                                                              #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2017                #
############################################################################
"""control lighting of our anteroom"""

### usage ###
# TODO
# sudo Anteroom.py

### setup ###
# TODO


import RPi.GPIO as io
import sys
import time

sys.path.append("../libs/")
from i2c import I2C
from actuators.PCA9685 import PCA9685, PCA9685_BASE_ADDRESS


###############################################################################
# PWM #########################################################################
class PWM (PCA9685):
    def __init__ (self, channel):
        # super().__init__(address=PCA9685_BASE_ADDRESS)
        super(PWM,self).__init__(address=PCA9685_BASE_ADDRESS)
        self.__channel = channel

    def set_pwm (self, on):
        # super().set_pwm(self.__channel, self.MAX-int(on), self.MAX)
        super(PWM,self).set_pwm(self.__channel, self.MAX-int(on), self.MAX)


###############################################################################
## main ######################################################################
pwm = PWM(0)

pin_ir = 7


io.setmode(io.BOARD)
io.setup(pin_ir, io.IN) 


last = None
while True:
    act = io.input(pin_ir)
    if act != last:
        if act == 1:
            pwm.set_pwm(PWM.MAX)
        else:
            pwm.set_pwm(PWM.MIN)

        last = act
        print("Status: {}".format(act))

    time.sleep(0.05)

# eof #

