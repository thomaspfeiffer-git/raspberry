#!/usr/bin/python3
# -*- coding: utf-8 -*-
###############################################################################
# Weatherstation.py                                                           #
# (c) https://github.com/thomaspfeiffer-git 2016                              #
###############################################################################
"""Weatherstation: collects various data from sensors in our flat and garden
   and displays them on a Tontec Touch Screen Display."""

import pygame
from pygame.locals import QUIT
import signal
import sys
from time import time
import traceback

sys.path.append('../libs')
from Config import CONFIG
from Display import Display
from Lightness import ControlLightness
from Screens import Screens

from SensorQueue import SensorQueueClient_read


###############################################################################
# Exit ########################################################################
def Exit():
    """stuff to be done on exit"""
    print("Exit")
    lightness.stop()
    lightness.join()
    pygame.quit()
    sys.exit()

def _Exit(__s, __f):
    """exit for signal handler"""
    print("_Exit")
    Exit()


###############################################################################
###############################################################################
class AllSensorValues (dict):
    """contains the (locally cached) values of all sensors and
       provides a method for polling the queue of the sensor values"""
    def __init__ (self, sensorqueue):
        super(AllSensorValues, self).__init__()
        self.__sensorqueue = sensorqueue
        self['ID_01'] = None
        self['ID_02'] = None
        self['ID_03'] = None
        self['ID_04'] = None
        self['ID_05'] = None
        self['ID_06'] = None
        self['ID_07'] = None
        self['ID_08'] = None
        self['ID_09'] = None
        self['ID_10'] = None
        self['ID_11'] = None
        self['ID_12'] = None
        self['ID_13'] = None
        self['ID_21'] = None
        self['ID_22'] = None
        self['ID_23'] = None
        self['ID_24'] = None
        self['ID_25'] = None
        self['ID_26'] = None
        self['ID_27'] = None
        self['ID_28'] = None
        self['ID_29'] = None
        self['ID_30'] = None
        self['ID_31'] = None
        self['ID_32'] = None
        self['ID_33'] = None
        self['ID_OWM_01'] = None
        self['ID_OWM_02'] = None
        self['ID_OWM_03'] = None
        self['ID_OWM_04'] = None
        self['ID_OWM_05'] = None
        self['ID_OWM_06'] = None
        self['ID_OWM_11'] = None
        self['ID_OWM_12'] = None
        self['ID_OWM_13'] = None
        self['ID_OWM_14'] = None
        self['ID_OWM_15'] = None
        self['ID_OWM_16'] = None
        self['ID_OWM_21'] = None
        self['ID_OWM_22'] = None
        self['ID_OWM_23'] = None
        self['ID_OWM_24'] = None
        self['ID_OWM_25'] = None
        self['ID_OWM_26'] = None

    def readfromqueue (self):
        """polls the queue for new sensor values (only one at a time)"""
        v = self.__sensorqueue.read() 
        if v is not None:
            self[v.id] = v


###############################################################################
# Main ########################################################################
def Main():
    """main program containing a loop for:
       - reading sensor values from the queue
       - update the screens accordingly
         . change screen on touch event
         . fallback to screen #1
         . update displayed values
    """
    display = Display()
    screens = Screens(display)

    allsensorvalues = AllSensorValues(SensorQueueClient_read())

    i = timestamp = 0
    while True:
        if (i >= 10):
            allsensorvalues.readfromqueue()

            if (time() >= timestamp): # fallback to screenid #1 
                screens.screenid = 1

            screens.drawScreen(allsensorvalues)
            i = 0

        for event in pygame.event.get():
            if event.type == QUIT:
                Exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not lightness.keypressed():
                    mouse = pygame.mouse.get_pos()
                    if display._button._rect.collidepoint(event.pos):
                        print("Button pressed: {} {}".format(event.pos, mouse))
                    else:
                        print("Clicked somewhere: {} {}".format(event.pos, mouse))

                        screens.screenid += 1
                        timestamp = time() + CONFIG.TIMETOFALLBACK

        pygame.time.delay(10)
        i += 1


###############################################################################
###############################################################################
if __name__ == '__main__':
    signal.signal(signal.SIGTERM, _Exit)

    try:
        lightness = ControlLightness()
        lightness.start()
        Main()

    except KeyboardInterrupt:
        Exit()

    except SystemExit:              # Done in signal handler (method _Exit()) #
        pass

    except:
        print(traceback.print_exc())

    finally:    # All cleanup is done in KeyboardInterrupt or signal handler. #
        pass

# eof #

