#!/usr/bin/python
# -*- coding: utf-8 -*-
###############################################################################
# weatherstation.py                                                           #
# (c) https://github.com/thomaspfeiffer-git 2016                              #
###############################################################################


import os
import pygame
from pygame.locals import QUIT
import RPi.GPIO as io
import signal
import sys
from time import sleep, time, strftime, localtime
import threading
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
###############################################################################
class Lightness (threading.Thread):
    def __init__ (self):
        threading.Thread.__init__(self)
        self.__lock = threading.Lock()
        self.__pin  = 18  # GPIO 18
        with self.__lock:
            self.__on = False
        self.__timestamp = time()

        io.setmode(io.BCM)
        io.setwarnings(False)
        io.setup(self.__pin, io.OUT)

        self.__running = True


    def __switch_on (self):
        io.output(self.__pin, 0)
        with self.__lock:
            self.__on = True
        self.__timestamp = time() + 15


    def __switch_off (self):
        if (time() > self.__timestamp):
            io.output(self.__pin, 1)
            with self.__lock:
                self.__on = False
            return True
        else:
            return False


    def run (self):
        while (self.__running):
            hour = int(strftime("%H", localtime()))
            if (hour >= 22) or (hour < 6):  # switch backlight off during night hours
                self.__switch_off()
            else:
                self.__switch_on()
           
            sleep(1)

        self.__switch_on()


    def stop (self):
        self.__switch_on()
        self.__running = False


    def keypressed (self):
        with self.__lock:
            on = self.__on
       
        if not on:
            self.__switch_on()
            return True
        else:
            return False
 

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

