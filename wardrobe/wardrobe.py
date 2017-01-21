#!/usr/bin/python3
# -*- coding: utf-8 -*-
#############################################################################
# wardrobe.py                                                               #
# (c) https://github.com/thomaspfeiffer-git 2017                            #
#############################################################################
"""controls lighting of my wardrobe"""

from enum import Enum
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
# #3        | pin 35  | bottom drawer (opt.)
# #4        | pin 37  | top area (opt.)
#
# debouncing:
# https://www.raspberrypi.org/forums/viewtopic.php?t=137484&p=913137
# http://raspberrypihobbyist.blogspot.co.at/2014/11/debouncing-gpio-input.html

Sensor1_Pin = 15   # phys pin id
Sensor2_Pin = 31
Sensor3_Pin = 35
Sensor4_Pin = 37

Actuator1_ID   = 0
Actuator2_ID   = 1
Actuator3_ID   = 2
Actuator4_ID   = 3


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
        self.__lock = threading.Lock()
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
            super().set_pwm(self.__channel, on, self.MAX)


###############################################################################
# Actuator ####################################################################
class Actuator (object):
    """turns light on and off (via PWM)"""

    def __init__ (self, pwm_id):
        self.pwm = PWM(pwm_id)
        self.__lightness = 0
        self.__stepsize = 40

    def _adjust_lightness (self):
        """adjust lightness value:
           - not greater than PWM.MAX
           - aligned to lightness measured by TSL2561"""

        max_lightness = (lightness.value+1) * 200

        if self.__lightness > max_lightness:
            self.__lightness = max_lightness

        if self.__lightness > PWM.MAX:
            self.__lightness = PWM.MAX

    def on (self):
        """door opened; lightness increases smoothly"""
        if self.__lightness < int(PWM.MAX / 4):
            self.__lightness += int(self.__stepsize/4)
        elif self.__lightness < int(PWM.MAX / 3):
            self.__lightness += int(self.__stepsize/3)
        elif self.__lightness < int(PWM.MAX / 2):
            self.__lightness += int(self.__stepsize/2)
        else:
            self.__lightness += self.__stepsize

        self._adjust_lightness()
        self.pwm.set_pwm(PWM.MAX-self.__lightness)
        # print("Actuator: set to on (lightness: {})".format(self.__lightness))

    def off (self):
        """door closed"""
        self.__lightness -= self.__stepsize
        if self.__lightness < PWM.MIN:
            self.__lightness = PWM.MIN
        self.pwm.set_pwm(PWM.MAX-self.__lightness)
        # print("Actuator: set to off (lightness: {})".format(self.__lightness))

    def immediate_off (self):
        """called on program exit"""
        self.__lightness = PWM.MIN
        self.off()


###############################################################################
# Control #####################################################################
class Control (threading.Thread):
    """detects an open door and switches light on"""

    def __init__ (self, sensor_id, actuator_id):
        threading.Thread.__init__(self)
        self.__lock     = threading.Lock()
        self.__sensor   = Sensor(sensor_id)
        self.__actuator = Actuator(actuator_id)

        self.__timestretched = time()
        self.__stretchperiod = 100

        self.__switch = Switch.OFF
        self.__sensor.start()

        self.__running = True

    def switchvalue_stretched (self):
        """enlarge interval of being "on"; otherwise if door is opened
           for a short period of time only, it would not be seen in RRD"""
        if time() <= self.__timestretched:
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
            self.__timestretched = time() + self.__stretchperiod
        with self.__lock:
            self.__switch = value    

    def run (self):
        while self.__running:
            self.switchvalue = self.__sensor.value

            if self.switchvalue == Switch.ON:
                self.__actuator.on()
            else:
                self.__actuator.off()
            sleep(0.02)

        self.__actuator.immediate_off() # Turn light off on exit.

    def stop (self):
        self.__running = False
        self.__sensor.stop()
        self.__sensor.join()


###############################################################################
# Main ########################################################################
def main ():
    cpu     = CPU()
    htu21df = HTU21DF()
    lightness.start()
    for c in controls:
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
                    ":{:}".format(controls[0].switchvalue_stretched())        + \
                    ":{}".format(0)                          + \
                    ":{:}".format(controls[1].switchvalue_stretched())        + \
                    ":{}".format(0)
        print(strftime("%Y%m%d %X:"), rrd_data)
        rrdtool.update(RRDFILE, "--template", rrd_template, rrd_data)

        sleep(50)


###############################################################################
# Exit ########################################################################
def _exit():
    """cleanup stuff"""
    for c in controls:
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
        controls  = []
        controls.append(Control(Sensor1_Pin, Actuator1_ID))
        # controls.append(Control(Sensor2_Pin, Actuator2_ID))
        controls.append(Control(Sensor3_Pin, Actuator3_ID))
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

