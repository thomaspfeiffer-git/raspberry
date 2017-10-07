#!/usr/bin/python3 -u
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


from enum import Enum
from flask import Flask, request
import rrdtool
import signal
import sys
import threading
from time import sleep, strftime, time

sys.path.append("../libs/")
from i2c import I2C
from Logging import Log
from Shutdown import Shutdown

from actuators.PCA9685 import PCA9685, PCA9685_BASE_ADDRESS
from sensors.CPU import CPU


# Misc for rrdtool
RRDFILE     = "/schild/weather/anteroom.rrd"
DS_SWITCH   = "ar_switch"
DS_TEMPCPU  = "ar_tempcpu"
DS_TEMP     = "ar_temp"
DS_HUMI     = "ar_humi"
DS_RES1     = "ar_res1"
DS_RES2     = "ar_res2"
DS_RES3     = "ar_res3"


app = Flask(__name__)


###############################################################################
# Switch ######################################################################
class Switch (Enum):
    OFF = 0
    ON  = 1


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
        self.stepsize  = 50

    def on (self):
        self.lightness += self.stepsize
        if self.lightness > PWM.MAX:
            self.lightness = PWM.MAX
        self.set_pwm(self.lightness)    

    def off (self):
        self.lightness -= self.stepsize
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
        self.__status = Switch.OFF
        self._timestretched = time()
        self._stretchperiod = 100

    @property
    def status (self):
        return self.__status

    @property
    def stretched_status (self):
        """Enlarge interval of being "on"; otherwise if switch is on
           for a short period of time only, it would not be seen in RRD."""
        if time() <= self._timestretched or self.status == Switch.ON:
            return Switch.ON 
        else:
            return Switch.OFF

    @status.setter
    def status (self, value):
        if self.status == Switch.OFF and value == Switch.ON:
            self._timestretched = time() + self._stretchperiod
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
            if relais.status == Switch.ON:
                self.leds.on()
            else:
                self.leds.off()
            sleep(0.05)

        # cleanup on exit
        self.leds.immediate_off()   # TODO: check in anderen programmen!

    def stop (self):
        self._running = False


###############################################################################
# Statistics ##################################################################
class Statistics (threading.Thread):
    rrd_template = DS_SWITCH  + ":" + \
                   DS_TEMPCPU + ":" + \
                   DS_TEMP    + ":" + \
                   DS_HUMI    + ":" + \
                   DS_RES1    + ":" + \
                   DS_RES2    + ":" + \
                   DS_RES3
    cpu = CPU()

    def __init__ (self):
        threading.Thread.__init__(self)
        self._running = True

    def run (self):    
        while self._running:
            rrd_data = "N:{}".format(relais.stretched_status.value)   + \
                        ":{:.2f}".format(self.cpu.read_temperature()) + \
                        ":{}".format(0.0)                             + \
                        ":{}".format(0.0)                             + \
                        ":{}".format(0.0)                             + \
                        ":{}".format(0.0)                             + \
                        ":{}".format(0.0)
            Log(rrd_data)
            rrdtool.update(RRDFILE, "--template", self.rrd_template, rrd_data)

            for _ in range(500): # interruptible sleep
                if self._running:
                    sleep(0.1)

    def stop (self):
        self._running = False


###############################################################################
# Flask stuff #################################################################
@app.route('/relais')
def API_Relais ():
    relais_ = request.args.get('status', 'off')
    Log("Request: relais={}".format(relais_))
    # TODO: validate param

    if relais_ == 'on':
        relais.status = Switch.ON
    else:
        relais.status = Switch.OFF
    return "OK. Status: {}".format(relais_)    


###############################################################################
# Exit ########################################################################
def shutdown_application ():
    """cleanup stuff"""

    for c in controls:
        c.stop()
        c.join()

    statistics.stop()
    statistics.join()

    sys.exit(0)


###############################################################################
## main #######################################################################
shutdown = Shutdown(shutdown_func=shutdown_application)

relais = Relais()
statistics = Statistics()
statistics.start()

controls = [ Control(channel) for channel in range(4) ]
for c in controls:
    c.start()

# eof #

