#!/usr/bin/python3
# -*- coding: utf-8 -*-
#############################################################################
# wardrobe.py                                                               #
# (c) https://github.com/thomaspfeiffer-git 2017                            #
#############################################################################
"""controls lighting of my wardrobe"""

from enum import Enum
import signal
import sys
from time import sleep
import threading
import traceback

sys.path.append("../libs/")
from i2c import I2C

# sensor id | gpio-in | gpio-out | usage |
# #1        | pin 15  | pin 16   | main area
# #2        | pin 31  | pin 32   | top drawer
# #3        | pin 35  | pin 36   | bottom drawer (opt.)
# #4        | pin 37  | pin 38   | top area (opt.)



# Lib: libs/pwm.py
# pin 12

# turtle/Reedcontact.py as example
# attention: has some logic for debouncing which causes a delay of 10 s
# until an opened door is recognized

# debouncing:
# https://www.raspberrypi.org/forums/viewtopic.php?t=137484&p=913137
# http://raspberrypihobbyist.blogspot.co.at/2014/11/debouncing-gpio-input.html


class Switch(Enum):
    OFF = 0
    ON  = 1


class Lightness (threading.Thread):
    """read lightness value from sensor"""
    """provide lightness value in getter method"""

    def __init__ (self):
        threading.Thread.__init__(self)
        self.__running = True

    def value (self):
        pass

    def run (self):
        while self.__running:
            pass

    def stop (self):
        self.__running = False


class Sensor (threading.Thread):
    """reads value of switch using GPIO"""

    def __init__ (self, pin):
        threading.Thread.__init__(self)
        self.__pin   = pin
        self.__lock  = threading.Lock()
        self.__value = Switch.OFF

        self.__running = True

    @property
    def value (self):
        with self.__lock:
            return self.__value

    def run (self):
        while self.__running:
            sleep(0.1) 
            # TODO: read gpio, maybe debouncing necessary


    def stop (self):
        self.__running = False



class Actor (I2C):
    """turns light on and off (via PWM)"""

    def __init__ (self, pwm_id):
        self.__pwm_id = pwm_id
        # Future:
        self.pwm = PWM(pwm_id)

    def on (self):
        pass

    def off (self):
        pass



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
            sleep(0.2)

        self.__actor.off() # Turn light off on exit.

    def stop (self):
        self.__running = False
        self.__sensor.stop()


###############################################################################
# Main ########################################################################
def main ():
    c1.start()
    while True:
        sleep(0.1)



###############################################################################
# Exit ########################################################################
def _exit():
    """cleanup stuff"""
    c1.stop()
    c1.join()
    sys.exit()

def __exit(__s, __f):
    """cleanup stuff used for signal handler"""
    _exit()


###############################################################################
###############################################################################
if __name__ == '__main__':
    signal.signal(signal.SIGTERM, __exit)

    try:
        c1 = Control(0, 0)
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

