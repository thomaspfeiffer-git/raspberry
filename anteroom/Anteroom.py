#!/usr/bin/python3
# -*- coding: utf-8 -*-
###############################################################################
# Anteroom.py                                                                 #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2017                   #
###############################################################################
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
import signal
import sys
import threading
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


###############################################################################
# LED_Strip ###################################################################
class LED_Strip (PWM):
    def __init__ (self, channel):
        super().__init__(channel)
        self.lightness = PWM.MIN
        self.stepsize  = 25

    def on (self):
        self.lightness += self.stepsize
        if self.lightness > PWM.MAX:
            self.lightness = PWM.MAX
        self.set_pwm(self.lightness)    

    def off (self):
        self.lightness -= int(self.stepsize / 2)
        if self.lightness < PWM.MIN:
            self.lightness = PWM.MIN
        self.set_pwm(self.lightness)

    def immediate_off (self):    
        self.lightness = PWM.MIN
        self.set_pwm(self.lightness)


###############################################################################
# Relais ######################################################################
class Relais (object):
    def __init__ (self):
        self.__status = 0

    @property
    def status (self):
        return self.__status

    @status.setter
    def status (self, value):
        self.__status = value


###############################################################################
# Control #####################################################################
class Control (threading.Thread):
    def __init__ (self, channel):
        threading.Thread.__init__(self)
        self.leds = LED_Strip(channel)
        self._running = True

    def run (self):
        while self._running:
            if relais.status == 1:
                self.leds.on()
            else:
                self.leds.off()
            time.sleep(0.05)    

    def stop (self):
        self._running = False
        self.leds.immediate_off()


###############################################################################
# Flask stuff #################################################################
@app.route('/relais')
def API_Relais ():
    relais_ = request.args.get('status', 'off')
    print("Request: relais={}".format(relais_))
    # TODO: validate param

    if relais_ == 'on':
        relais.status = 1
    else:
        relais.status = 0
    return "OK. Status: {}".format(relais_)    


###############################################################################
# Exit ########################################################################
def _exit ():
    """cleanup stuff"""
    control.stop()
    control.join()
    sys.exit(0)

def __exit (__s, __f):
    """cleanup stuff used for signal handler"""
    _exit()


###############################################################################
## main ######################################################################
signal.signal(signal.SIGTERM, __exit)
signal.signal(signal.SIGINT, __exit)

relais = Relais()
control = Control(0)
control.start()

# eof #

