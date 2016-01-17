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
from pwm import PWM


###############################################################################
###############################################################################
class Lightness (threading.Thread):
    """controls lightness of Tontec Touch Screen Display"""
    """currently display is switched off between 10 pm and 6 am"""

    DELAYTOLIGHTOFF = 15

    def __init__ (self):
        threading.Thread.__init__(self)
        self.__lock = threading.Lock()
        self.__pwm  = PWM()
        with self.__lock:
            self.__on = False
        self.__timestamp = time()

        self.__running = True


    def __switch_on (self):
        """turn backlight on"""
        self.__pwm.on()
        with self.__lock:
            self.__on = True
        self.__timestamp = time() + self.DELAYTOLIGHTOFF


    def __switch_off (self):
        """turn backlight off only if DELAYTOLIGHTOFF seconds 
           have passed after switch on"""
        if (time() > self.__timestamp):
            self.__pwm.off()
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
            sleep(1)
          
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
        else:              # of Lightness.keypressed().
            return False

# eof #
