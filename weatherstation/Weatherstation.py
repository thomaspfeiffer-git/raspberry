#!/usr/bin/python
# -*- coding: utf-8 -*-
###############################################################################
# weatherstation.py                                                           #
# (c) https://github.com/thomaspfeiffer-git 2016                              #
###############################################################################



"""TODO: Backlight on/off

import RPi.GPIO as io
from time import sleep

io.setmode(io.BCM)
io.setup(18,io.OUT)

while True:
    io.output(18,1)
    sleep(1)
    io.output(18,0)
    sleep(1)


class Lightness (def):
    def __init__(self):
        pass

    def Touched (self):
        if user touches screen:
            if light == off: 
                light_on()
                after n seconds
                light_off()

    todos:
        a) based on lightness switch backlight automatically on/off
        b) based on time of day switch backlight automatically on/off


"""



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
from Screens import Screens

from SensorQueue import SensorQueueClient_read


###############################################################################
# Exit ########################################################################
def Exit():
    """stuff to be done on exit"""
    print("Exit")
    pygame.quit()
    sys.exit()

def _Exit(__s, __f):
    """exit for signal handler"""
    print("_Exit")
    Exit()


###############################################################################
###############################################################################
class AllSensorValues (dict):
    def __init__ (self, sensorqueue):
        super(dict, self).__init__()
        self.__sensorqueue = sensorqueue
        self['ID_01'] = "(n/a)"
        self['ID_02'] = "(n/a)"
        self['ID_03'] = "(n/a)"
        self['ID_04'] = "(n/a)"
        self['ID_05'] = "(n/a)"
        self['ID_06'] = "(n/a)"
        self['ID_07'] = "(n/a)"
        self['ID_08'] = "(n/a)"
        self['ID_09'] = "(n/a)"
        self['ID_10'] = "(n/a)"
        self['ID_11'] = "(n/a)"
        self['ID_12'] = "(n/a)"

    def readfromqueue (self):
        v = self.__sensorqueue.read() 
        if v is not None:
            # TODO: check age of data
            # if timestamp <= now() + 1 h: sensorvalue[x] = "n/a"
            # self.__sensorvalues[v.getID()] = v.value.encode('latin-1')
            self[v.getID()] = v.value.encode('latin-1')


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
                screens.screenid += 1
                timestamp = time() + CONFIG.TIMETOFALLBACK

        pygame.time.delay(10)
        i += 1


###############################################################################
###############################################################################
if __name__ == '__main__':
    signal.signal(signal.SIGTERM, _Exit)

    try:
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

