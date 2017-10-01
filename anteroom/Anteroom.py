#!/usr/bin/python3
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


from flask import Flask
import sys
import time

sys.path.append("../libs/")
from i2c import I2C
from actuators.PCA9685 import PCA9685, PCA9685_BASE_ADDRESS


app = Flask(__name__)


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


############################################################################
# Flask stuff ##############################################################
@app.route('/relais')
    relais = int(request.args.get('status', 'off'))  
    # TODO: validate param





###############################################################################
## main ######################################################################
pwm = PWM(0)







# eof #

