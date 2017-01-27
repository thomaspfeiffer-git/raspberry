#!/usr/bin/python3
# -*- coding: utf-8 -*-
#############################################################################
# wardrobe.py                                                               #
# (c) https://github.com/thomaspfeiffer-git 2017                            #
#############################################################################
"""controls lighting of my wardrobe"""

from enum import Enum
from math import pi, sin, asin
import RPi.GPIO as io
import rrdtool
import signal
import sys
import threading
from time import sleep, strftime, time
import traceback


sys.path.append("../libs/")
from i2c import I2C
from actuators.PCA9685 import PCA9685, PCA9685_BASE_ADDRESS
from actuators.SSD1306 import SSD1306
from sensors.CPU import CPU
from sensors.HTU21DF import HTU21DF
from sensors.TSL2561 import TSL2561 


# sensor id | gpio-in | usage |
# #1        | pin 15  | main area
# #2        | pin 31  | top drawer
# #3        | pin 35  | button for full lightness
# #4        | pin 37  | unused
#
# debouncing:
# https://www.raspberrypi.org/forums/viewtopic.php?t=137484&p=913137
# http://raspberrypihobbyist.blogspot.co.at/2014/11/debouncing-gpio-input.html

Sensor1_Pin = 15   # phys pin id
Sensor2_Pin = 31
Sensor3_Pin = 35
Sensor4_Pin = 37

Actuator1_ID = 0
Actuator2_ID = 1
Actuator3_ID = 2
Actuator4_ID = 3


# Misc for rrdtool
RRDFILE      = "/schild/weather/wardrobe.rrd"
DS_TEMP1     = "wr_temp1"
DS_TEMPCPU   = "wr_tempcpu"
DS_TEMP2     = "wr_temp2"
DS_HUMI      = "wr_humi"
DS_LIGHTNESS = "wr_lightness"
DS_OPEN1     = "wr_open1"
DS_OPEN2     = "wr_open2"
DS_OPEN3     = "wr_open3"
DS_OPEN4     = "wr_open4"


# I2C._lock() works on a very low level, so an additional locking
# is needed (which makes I2C._lock() quite redundant unfortunately).
central_i2c_lock = threading.Lock()


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
            with central_i2c_lock:
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
        self.__lock  = threading.Lock()
        self.__pin   = pin
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
        super().__init__(address=PCA9685_BASE_ADDRESS+1)
        self.__channel = channel

    def set_pwm (self, on):
        with central_i2c_lock:
            super().set_pwm(self.__channel, int(on), self.MAX)


###############################################################################
# Smooth ######################################################################
class Smooth (object):
    """smoothes lights on/off following a sinus curve"""

    def __init__ (self, stepsize=0.01):
        self.__pwmmax     = PWM.MAX / 2.0
        self.__countermax = pi / 2.0
        self.__countermin = -self.__countermax
        self.__counter    = self.__countermin
        self.__stepsize   = stepsize

    def increase (self):
        self.__counter += self.__stepsize
        if self.__counter > self.__countermax:
            self.__counter = self.__countermax

    def decrease (self):
        self.__counter -= self.__stepsize
        if self.__counter < self.__countermin:
            self.__counter = self.__countermin

    @property
    def lightness (self):
        return sin(self.__counter) * self.__pwmmax + self.__pwmmax

    @lightness.setter
    def lightness (self, value):
        self.__counter = asin((value - self.__pwmmax) / self.__pwmmax)


###############################################################################
# Actuator ####################################################################
class Actuator (object):
    """turns light on and off (via PWM)"""

    def __init__ (self, pwm_id):
        self.pwm    = PWM(pwm_id)
        self.smooth = Smooth()

    def adjust_lightness (self, off=False):
        """adjust lightness value:
           - aligned to lightness measured by TSL2561
           - not greater than PWM.MAX
           - set to max lightness if button was pressed"""

        max_lightness = (lightness.value+1) * 50
        if self.smooth.lightness > max_lightness:
            self.smooth.lightness = max_lightness

        if self.smooth.lightness > PWM.MAX:
            self.smooth.lightness = PWM.MAX

        try: 
            if not off:  # when switching off, 
                         # lightness is supposed to normal level
                         # (means: no lightness overule on off).
                if controls['button'].switchvalue_stretched() == 1:
                    self.smooth.lightness = PWM.MAX
        except (NameError):
            pass

    def on (self, lightnessvalue=0):
        """door opened"""
        if lightnessvalue == 0:
            self.smooth.increase()
        else:
            self.smooth.lightness = lightnessvalue

        self.adjust_lightness()
        self.pwm.set_pwm(PWM.MAX-self.smooth.lightness)

    def off (self):
        """door closed"""
        self.smooth.decrease()
        self.adjust_lightness(off=True)
        self.pwm.set_pwm(PWM.MAX-self.smooth.lightness)

    def immediate_off (self):
        """called on program exit"""
        self.smooth.lightness = PWM.MIN
        self.pwm.set_pwm(PWM.MAX-self.smooth.lightness)


###############################################################################
# Control #####################################################################
class Control (threading.Thread):
    """detects an open door and switches light on"""

    def __init__ (self, sensor_id, actuator_id):
        threading.Thread.__init__(self)
        self.__lock    = threading.Lock()
        self._sensor   = Sensor(sensor_id)
        self._actuator = Actuator(actuator_id)
        self._actuator.off()

        self._timestretched = time()
        self._stretchperiod = 100

        self.__switch = Switch.OFF
        self._sensor.start()

        self._running = True

    def switchvalue_stretched (self):
        """Enlarge interval of being "on"; otherwise if door is opened
           for a short period of time only, it would not be seen in RRD.
           In case of Control_Button (derived from Control), this method
           indicates full lightness."""
        if time() <= self._timestretched:
            return 1
        else:
            return 0

    @property
    def switchvalue (self):
        with self.__lock:
            return self.__switch    

    @switchvalue.setter
    def switchvalue (self, value):
        if (self.switchvalue == Switch.OFF and value == Switch.ON) \
            or self.switchvalue == Switch.ON:
            self._timestretched = time() + self._stretchperiod
        with self.__lock:
            self.__switch = value    

    def run (self):
        while self._running:
            self.switchvalue = self._sensor.value

            if self.switchvalue == Switch.ON:
                self._actuator.on()
            else:
                self._actuator.off()
            sleep(0.02)

        self._actuator.immediate_off() # Turn light off on exit.

    def stop (self):
        self._running = False
        self._sensor.stop()
        self._sensor.join()


###############################################################################
# Control_Button ##############################################################
class Control_Button (Control):
    def __init__ (self, sensor_id, actuator_id):
        super().__init__(sensor_id, actuator_id)
        self._stretchperiod = 60

    def run (self):
        self._actuator.on(lightnessvalue=PWM.MAX)  # constant actuator output
        while self._running:
            self.switchvalue = self._sensor.value
            sleep(0.02)


###############################################################################
# Main ########################################################################
def main ():
    cpu     = CPU()
    htu21df = HTU21DF()
    lightness.start()
    for c in controls.values():
        c.start()

    rrd_template = DS_TEMP1     + ":" + \
                   DS_TEMPCPU   + ":" + \
                   DS_TEMP2     + ":" + \
                   DS_HUMI      + ":" + \
                   DS_LIGHTNESS + ":" + \
                   DS_OPEN1     + ":" + \
                   DS_OPEN2     + ":" + \
                   DS_OPEN3     + ":" + \
                   DS_OPEN4

    while True:
        with central_i2c_lock:
            htu21df_temperature = htu21df.read_temperature()
            htu21df_humidity    = htu21df.read_humidity()

        rrd_data = "N:{:.2f}".format(htu21df_temperature)    + \
                    ":{:.2f}".format(cpu.read_temperature()) + \
                    ":{:.2f}".format(99.99)                  + \
                    ":{:.2f}".format(htu21df_humidity)       + \
                    ":{:.2f}".format(lightness.value)        + \
                    ":{}".format(controls['doors'].switchvalue_stretched())  + \
                    ":{}".format(0)                          + \
                    ":{}".format(controls['drawer'].switchvalue_stretched()) + \
                    ":{}".format(0)
        print(strftime("%Y%m%d %X:"), rrd_data)
        rrdtool.update(RRDFILE, "--template", rrd_template, rrd_data)

        sleep(50)


###############################################################################
# Exit ########################################################################
def _exit():
    """cleanup stuff"""
    for c in controls.values():
        c.stop()
        c.join()

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
        controls  = {
                     'doors':  Control(Sensor1_Pin, Actuator1_ID),
                     'drawer': Control(Sensor2_Pin, Actuator2_ID),
                     'button': Control_Button(Sensor3_Pin, Actuator3_ID)
                    }
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

