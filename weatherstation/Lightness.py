# -*- coding: utf-8 -*-
################################################################################
# Lightness.py                                                                 #
# (c) https://github.com/thomaspfeiffer-git 2016                               #
################################################################################
"""controls lightness of Tontec Touch Screen Display via PWM"""

import sys
import threading
from time import sleep, time, strftime, localtime

sys.path.append('../libs')
sys.path.append('../libs/sensors')

from Measurements import Measurements
from PCF8591 import PCF8591
from pwm import PWM


###############################################################################
class Sensor (object):
    """Reads data from A/D Converter (PCD8591). In order to smooth transitions
       from dark to bright and bright to dark, the average of 20 sensor values 
       is used for lightness control"""
       
    def __init__ (self):
        self.__adc = PCF8591(0x48)
        self.__measurements = Measurements(maxlen=20)

    def read (self):
        """read ADC and update deque for averaging"""
        v = 1024 - (self.__adc.read() * 4)
        if v > 1020:
            v = 1020
        self.__measurements.append(v)
        return self.__measurements.avg() 


###############################################################################
class ControlLightness (threading.Thread):
    """controls lightness of Tontec Touch Screen Display"""

    DELAYTOLIGHTOFF = 15.0

    def __init__ (self):
        threading.Thread.__init__(self)

        self.__lock   = threading.Lock()
        self.__sensor = Sensor()
        self.__pwm    = PWM()

        with self.__lock:
            self.__on = False
        self.__timestamp = time()

        self.__running = True


    def __switch_on (self):
        """switch backlight on and set timestamp in order to switch off
           after self.DELAYTOLIGHTOFF seconds at the earliest"""
        self.__pwm.on()
        with self.__lock:
            self.__on = True
        self.__timestamp = time() + self.DELAYTOLIGHTOFF


    def __switch_off (self):
        """control backlight according to lightness only 
           if DELAYTOLIGHTOFF seconds have passed after switch on"""
        if (time() > self.__timestamp):
            self.__pwm.control(self.__sensor.read())
            with self.__lock:
                self.__on = False
            return True
        else:
            return False


    def run (self):
        """main routine of thread"""
        while (self.__running):

            hour = int(strftime("%H", localtime()))
            if (hour >= 22) or (hour < 6):  # switch backlight off during night hours
                self.__switch_off()
            else:
                self.__switch_on()
            sleep(0.02)
          
        # switch backlight on on exit 
        # (otherwise the display might be very dark :-) )
        self.__switch_on() 


    def stop (self):
        """stops thread and switches backlight on"""
        self.__switch_on()
        self.__running = False


    def keypressed (self):
        """touching the display switches backlight on"""
        with self.__lock:
            already_on = self.__on
        self.__switch_on()
       
        if not already_on: # if the backlight was alread on, touch 
            return True    # event has to be processed by the caller 
        else:              # of ControlLightness.keypressed().
            return False

# eof #

