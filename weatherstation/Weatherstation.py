#!/usr/bin/python3
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



def read_sensorvalues (sq, sensorvalues):
    v = sq.read() 
    if v is not None:
        sensorvalues[v.getID()] = v



###############################################################################
# Main ########################################################################
def Main():
    os.environ["SDL_FBDEV"] = "/dev/fb1"
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    pygame.mouse.set_visible(False)

    display = Display()
    screens = Screens(display)

    sq = SensorQueueClient_read()
    sensorvalues = {}

    i = timestamp = 0
    while True:
        if (i >= 10):
            read_sensorvalues(sq, sensorvalues)
            for v in sensorvalues:
                print(v)

            if (time() >= timestamp): # fallback to screenid #1 
                screens.screenid = 1

            screens.Screen()
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

