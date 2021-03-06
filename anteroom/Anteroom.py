#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# Anteroom.py                                                                 #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2017, 2019, 2020       #
###############################################################################
"""control lighting of our anteroom"""

### usage ###
# nohup ./Anteroom.py >Anteroom.log 2>&1 &


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
import signal
import subprocess
import sys
import threading
from time import sleep, strftime, time

sys.path.append("../libs/")
from gpio import gpio as io
from i2c import I2C
from Logging import Log
from Shutdown import Shutdown

from actuators.PCA9685 import PCA9685, PCA9685_BASE_ADDRESS
from sensors.CPU import CPU

from Anteroom_UDP import Sender

app = Flask(__name__)

pin_fan = 198    # Phys pin 8


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
        self.stepsize  = 30

    def on (self):
        self.lightness += self.stepsize * 2
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
        self._timestamp_on  = 0
        self._timestamp_off = 0

    @property
    def status (self):
        return self.__status

    def status_stretchoff (self, stretchvalue=120):
        """Delay off for a couple of seconds."""
        if self._timestamp_off + stretchvalue > time() or self.status == Switch.ON:
            return Switch.ON
        else:
            return Switch.OFF

    def status_stretchon (self, stretchvalue=120):
        """Enlarge interval of being "on"; otherwise if switch would be on
           for a short period of time only, it would not be seen in RRD."""
        if self._timestamp_on + stretchvalue > time() or self.status == Switch.ON:
            return Switch.ON
        else:
            return Switch.OFF

    @status.setter
    def status (self, value):
        if self.status == Switch.OFF and value == Switch.ON:
            self._timestamp_on = time()
        if self.status == Switch.ON and value == Switch.OFF:
            self._timestamp_off = time()
        self.__status = value


###############################################################################
# SaveEnergy ##################################################################
class SaveEnergy (object):
    """if LEDs are switched on using the button AND time.hour >= 21:
       do not switch on all four LED strips
    """

    def __init__ (self):
        self.reset()

    def set (self):
        self.__active = True

    def reset (self):
        self.__active = False

    def __call__ (self):
        return self.__active and (int(strftime("%H")) >= 21 or int(strftime("%H")) <= 4)


###############################################################################
# Control #####################################################################
class Control (threading.Thread):
    def __init__ (self, channel, powersaving=False):
        threading.Thread.__init__(self)
        self.leds = LED_Strip(channel)
        self.__powersaving = powersaving

    def run (self):
        self._running = True
        while self._running:
            if relais.status_stretchoff(stretchvalue=3) == Switch.ON:
                if save_energy():
                    if not self.__powersaving:
                        self.leds.on()
                else:
                    self.leds.on()
            else:
                self.leds.off()
            sleep(0.05)

        # cleanup on exit
        self.leds.immediate_off()

    def stop (self):
        self._running = False


###############################################################################
# Fan #########################################################################
class Fan (threading.Thread):
    def __init__ (self, pin):
        threading.Thread.__init__(self)
        self.__fan = io(pin, io.OUT)
        self.__last = None
        self.off()

    def on (self):
        if self.__last != Switch.ON:
            self.__fan.write("0")
            self.__last = Switch.ON

    def off (self):
        if self.__last != Switch.OFF:
            self.__fan.write("1")
            self.__last = Switch.OFF

    def run (self):
        self._running = True
        while self._running:
            if relais.status_stretchoff() == Switch.ON:
                self.on()
            else:
                self.off()
            sleep(0.1)
        self.off()
        self.__fan.close()

    def stop (self):
        self._running = False


###############################################################################
# Statistics ##################################################################
class Statistics (threading.Thread):
    cpu = CPU()

    def __init__ (self):
        threading.Thread.__init__(self)
        self.udp = Sender()

    def run (self):
        self._running = True
        while self._running:
            rrd_data = "N:{}".format(relais.status_stretchon().value) + \
                        ":{:.2f}".format(self.cpu.read_temperature()) + \
                        ":{}".format(0.0)                             + \
                        ":{}".format(0.0)                             + \
                        ":{}".format(0.0)                             + \
                        ":{}".format(0.0)                             + \
                        ":{}".format(0.0)
            Log(rrd_data, True)
            self.udp.send(rrd_data)

            for _ in range(500): # interruptible sleep
                if self._running:
                    sleep(0.1)
                else:
                    break

    def stop (self):
        self._running = False


###############################################################################
# Flask stuff #################################################################
@app.route('/relais')
def API_Relais ():
    relais_ = request.args.get('status', 'off')
    Log("Request: relais={}".format(relais_), True)
    # TODO: validate param

    save_energy.reset()

    if relais_ == 'on':
        relais.status = Switch.ON
    else:
        relais.status = Switch.OFF

    return "OK. Status: {}".format(relais_)


@app.route('/toggle')
def API_Toggle ():
    triggered_by_button = request.args.get("button", "0") == "1"

    save_energy.reset()

    if relais.status == Switch.ON:
        relais.status = Switch.OFF
    else:
        relais.status = Switch.ON
        if triggered_by_button:
            save_energy.set()

    Log("Request: toggle to {}; triggered by button: {}".format(relais.status, triggered_by_button))
    return "OK. Status: {}".format(relais.status)



###############################################################################
# Exit ########################################################################
def shutdown_application ():
    """cleanup stuff"""

    for c in controls:
        c.stop()
        c.join()

    statistics.stop()
    statistics.join()
    fan.stop()
    fan.join()

    sys.exit(0)


###############################################################################
## main #######################################################################
if __name__ == "__main__":
    shutdown = Shutdown(shutdown_func=shutdown_application)

    save_energy = SaveEnergy()
    relais = Relais()
    fan = Fan(pin_fan)
    fan.start()
    statistics = Statistics()
    statistics.start()

    controls = [ Control(channel, powersaving=channel!=1) for channel in range(4) ]
    for c in controls:
        c.start()

    app.run(host="0.0.0.0")

# eof #

