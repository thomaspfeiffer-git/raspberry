#!/usr/bin/python
# -*- coding: utf-8 -*-
###############################################################################
# weatherstation.py                                                           #
# (c) https://github.com/thomaspfeiffer-git 2016                              #
###############################################################################


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



class AllSensorValues (object):
    def __init__ (self, sensorqueue):
        self.__sensorqueue = sensorqueue
        self.__sensorvalues = {'ID_01': "n/a", \
                               'ID_02': "n/a", \
                               'ID_03': "n/a", \
                               'ID_04': "n/a", \
                               'ID_05': "n/a"}

    def readfromqueue (self):
        v = self.__sensorqueue.read() 
        if v is not None:
            self.__sensorvalues[v.getID()] = v.value.encode('latin-1')

    def read (self, sid):
        return self.__sensorvalues[sid]



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
            for s in ['ID_01', 'ID_02', 'ID_03', 'ID_04', 'ID_05']:
                print s, ":", allsensorvalues.read(s)

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

        pygame.time.delay(50)
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

