#!/usr/bin/python3
# -*- coding: utf-8 -*-
#############################################################################
# wardrobe.py                                                               #
# (c) https://github.com/thomaspfeiffer-git 2017                            #
#############################################################################
"""controls lighting of my wardrobe"""

from enum import Enum
import RPi.GPIO as io
import signal
import sys
from time import sleep
import threading
import traceback

sys.path.append("../libs/")
from i2c import I2C
from actors.PCA9685 import PCA9685
from sensors.TSL2561 import TSL2561 


# sensor id | gpio-in | gpio-out | usage |
# #1        | pin 15  | pin 16   | main area
# #2        | pin 31  | pin 32   | top drawer
# #3        | pin 35  | pin 36   | bottom drawer (opt.)
# #4        | pin 37  | pin 38   | top area (opt.)

Sensor1_Pin = 15   # phys pin id
Sensor2_Pin = 31
Sensor3_Pin = 35
Sensor4_Pin = 37

Actor1_ID   = 0
Actor2_ID   = 1
Actor3_ID   = 2
Actor4_ID   = 3

# gpio -1 mode 15 in
# gpio -1 read 15

# debouncing:
# https://www.raspberrypi.org/forums/viewtopic.php?t=137484&p=913137
# http://raspberrypihobbyist.blogspot.co.at/2014/11/debouncing-gpio-input.html


class Switch (Enum):
    OFF = 0
    ON  = 1


###############################################################################
# Lightness ###################################################################
class Lightness (threading.Thread):
    """read lightness value from sensor"""
    """provide lightness value in getter method"""

    def __init__ (self):
        threading.Thread.__init__(self)
        self.__lock    = threading.Lock()
        self.__tsl2561 = TSL2561()
        self.__value   = 0
        self.__running = True

    @property
    def value (self):
        with self.__lock:
            return self.__value

    def run (self):
        while self.__running:
            v = self.__tsl2561.lux()
            with self.__lock:
                self.__value = v
            sleep(1)

    def stop (self):
        self.__running = False


###############################################################################
# Sensor ######################################################################
class Sensor (threading.Thread):
    """reads value of switch using GPIO"""

    def __init__ (self, pin):
        threading.Thread.__init__(self)
        self.__pin   = pin
        self.__lock  = threading.Lock()
        self.__value = Switch.OFF

        io.setmode(io.BOARD)
        io.setup(self.__pin, io.IN)
        io.setup(self.__pin, io.IN, pull_up_down=io.PUD_UP)

        self.__running = True

    @property
    def value (self):
        with self.__lock:
            return self.__value

    def run (self):
        while self.__running:
            v = Switch.OFF if io.input(self.__pin) == 0 else Switch.ON
            with self.__lock:
                self.__value = v
            sleep(0.1) 

    def stop (self):
        self.__running = False


###############################################################################
# PWM #########################################################################
class PWM (PCA9685):
    def __init__ (self, channel):
        super().__init__()
        self.__channel = channel

    def set_pwm (self, on):
        super().set_pwm(self.__channel, on, self.MAX)


###############################################################################
# Actor #######################################################################
class Actor (object):
    """turns light on and off (via PWM)"""

    def __init__ (self, pwm_id):
        self.pwm = PWM(pwm_id)
        self.__lightness = 0
        self.__stepsize = 40

    def on (self):
        if self.__lightness < int(PWM.MAX / 4):
            self.__lightness += int(self.__stepsize/4)
        elif self.__lightness < int(PWM.MAX / 3):
            self.__lightness += int(self.__stepsize/3)
        elif self.__lightness < int(PWM.MAX / 2):
            self.__lightness += int(self.__stepsize/2)
        else:
            self.__lightness += self.__stepsize
        if self.__lightness > PWM.MAX:
            self.__lightness = PWM.MAX
        self.pwm.set_pwm(PWM.MAX-self.__lightness)
        print("Actor: set to on (lightness: {})".format(self.__lightness))

    def off (self):
        self.__lightness -= self.__stepsize
        if self.__lightness < PWM.MIN:
            self.__lightness = PWM.MIN
        self.pwm.set_pwm(PWM.MAX-self.__lightness)
        print("Actor: set to off (lightness: {})".format(self.__lightness))

    def immediate_off (self):
        self.__lightness = PWM.MIN
        self.off()


###############################################################################
# Control #####################################################################
class Control (threading.Thread):
    """detects an open door and switches light on"""

    def __init__ (self, sensor_id, actor_id):
        threading.Thread.__init__(self)
        self.__sensor = Sensor(sensor_id)
        self.__actor  = Actor(actor_id)

        self.__sensor.start()

        self.__running = True

    def run (self):
        while self.__running:
            switch = self.__sensor.value
            if switch == Switch.ON:
                self.__actor.on()
            else:
                self.__actor.off()
            sleep(0.02)

        self.__actor.immediate_off() # Turn light off on exit.

    def stop (self):
        self.__running = False
        self.__sensor.stop()


###############################################################################
# Main ########################################################################
def main ():
    lightness.start()
    c1.start()
    while True:
        sleep(0.1)


###############################################################################
# Exit ########################################################################
def _exit():
    """cleanup stuff"""
    c1.stop()
    c1.join()
    lightness.stop()
    lightness.join()
    sys.exit()

def __exit(__s, __f):
    """cleanup stuff used for signal handler"""
    _exit()


###############################################################################
###############################################################################
if __name__ == '__main__':
    signal.signal(signal.SIGTERM, __exit)

    try:
        lightness = Lightness()
        c1 = Control(Sensor1_Pin, Actor1_ID)
        main()

    except KeyboardInterrupt:
        _exit()

    except SystemExit:              # Done in signal handler (method _exit()) #
        pass

    except:
        print(traceback.print_exc())
        _exit()

    finally:    # All cleanup is done in KeyboardInterrupt or signal handler. #
        pass

# eof #

