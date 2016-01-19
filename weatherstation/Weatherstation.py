#!/usr/bin/python
# -*- coding: utf-8 -*-
###############################################################################
# Weatherstation.py                                                           #
# (c) https://github.com/thomaspfeiffer-git 2016                              #
###############################################################################
"""Weatherstation: collects various data from sensors in our flat and garden
   and displays them on a Tontec Touch Screen Display."""

import os
import pygame
from pygame.locals import QUIT
import signal
import sys
from time import time
import traceback

sys.path.append('../libs')
from Config import CONFIG
from Display import Display
from Lightness import Lightness
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
class ValueCache (object):
    def __init__ (self, value):
        self.__value     = None
        self.__timestamp = None
        self.value       = value

    @property
    def value (self):
        if self.__timestamp + 60 < time(): # data is older than 60 seconds
            return "n/a".encode('latin-1')
        else:
            return self.__value

    @value.setter
    def value (self, value):
        self.__value     = value
        self.__timestamp = time()
    


###############################################################################
###############################################################################
class AllSensorValues (dict):
    def __init__ (self, sensorqueue):
        super(AllSensorValues, self).__init__()
        self.__sensorqueue = sensorqueue
        self['ID_01'] = "(n/a)".encode('latin-1')
        self['ID_02'] = "(n/a)".encode('latin-1')
        self['ID_03'] = "(n/a)".encode('latin-1')
        self['ID_04'] = "(n/a)".encode('latin-1')
        self['ID_05'] = "(n/a)".encode('latin-1')
        self['ID_06'] = "(n/a)".encode('latin-1')
        self['ID_07'] = "(n/a)".encode('latin-1')
        self['ID_08'] = "(n/a)".encode('latin-1')
        self['ID_09'] = "(n/a)".encode('latin-1')
        self['ID_10'] = "(n/a)".encode('latin-1')
        self['ID_11'] = "(n/a)".encode('latin-1')
        self['ID_12'] = "(n/a)".encode('latin-1')

    def readfromqueue (self):
        v = self.__sensorqueue.read() 
        if v is not None:
            self[v.getID()] = v.value.encode('latin-1')

            # TODO: check age of data 
            #if v.getTimestamp() < time() + 60: 
            #    self[v.getID()] = v.value.encode('latin-1')
            #else:
            #    self[v.getID()] = "n/a".encode('latin-1')


###############################################################################
# Main ########################################################################
def Main():
    os.environ["SDL_FBDEV"] = "/dev/fb1"
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    pygame.mouse.set_visible(False)

    display = Display()
    screens = Screens(display)

    allsensorvalues = AllSensorValues(SensorQueueClient_read())

    i = timestamp = 0
    while True:
        if (i >= 10):
            allsensorvalues.readfromqueue()

            if (time() >= timestamp): # fallback to screenid #1 
                screens.screenid = 1

            screens.Screen(allsensorvalues)
            pygame.display.update()
            i = 0

        for event in pygame.event.get():
            if event.type == QUIT:
                Exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not lightness.keypressed():
                    screens.screenid += 1
                    timestamp = time() + CONFIG.TIMETOFALLBACK

        pygame.time.delay(10)
        i += 1


###############################################################################
###############################################################################
if __name__ == '__main__':
    signal.signal(signal.SIGTERM, _Exit)

    try:
        lightness = Lightness()
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

