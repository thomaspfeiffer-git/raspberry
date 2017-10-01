#!/usr/bin/python3
# -*- coding: utf-8 -*-
############################################################################
# Anteroom.py                                                              #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2017                #
############################################################################
"""control lighting of our anteroom"""

### usage ###
# sudo bash
# export FLASK_APP=Anteroom.py
# flask run --host=0.0.0.0 >Anteroom.log 2>&1 &


### setup ###
# http://flask.pocoo.org/docs/0.12/
#
# http://jinja.pocoo.org/docs/2.9/
# sudo pip3 install Jinja2
#
# http://werkzeug.pocoo.org/docs/0.11/
# sudo pip3 install Werkzeug
#
# http://flask.pocoo.org/docs/0.12/
# sudo pip3 install Flask


from flask import Flask, request
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
        super().__init__(address=PCA9685_BASE_ADDRESS)
        self.__channel = channel

    def set_pwm (self, on):
        super().set_pwm(self.__channel, self.MAX-int(on), self.MAX)


############################################################################
# Flask stuff ##############################################################
@app.route('/relais')
def Relais ():
    relais = request.args.get('status', 'off')
    print("Request: relais={}".format(relais))
    # TODO: validate param

    if relais == 'on':
        pwm.set_pwm(PWM.MIN)
        # pwm.set_pwm(PWM.MAX)
    else:
        pwm.set_pwm(PWM.MIN)
    return "ok"    



###############################################################################
## main ######################################################################
pwm = PWM(0)







# eof #

