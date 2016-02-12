#!/usr/bin/python3
# -*- coding: utf-8 -*-
###############################################################################
# test_i2c_concurrency.py                                                     #
# (c) https://github.com/thomaspfeiffer-git 2016                              #
###############################################################################
"""Test concurrency issues on the I2C bus with the Tontec Display"""

import os
import pygame
import signal
import sys
import threading
from time import sleep, gmtime, strftime
import traceback

sys.path.append('../libs')
sys.path.append('../libs/sensors')

from PCF8591 import PCF8591



###############################################################################
class ReadI2C (threading.Thread):
    def __init__ (self):
        threading.Thread.__init__(self)
        self._adc = PCF8591(0x48)

        self.__running = True

    def run (self):
        while self.__running:
            v = self._adc.read()
            # print("Value ADC: %i" % v) 

    def stop (self):
        self.__running = False



###############################################################################
class Display (object):
    def __init__ (self):
        os.environ["SDL_FBDEV"] = "/dev/fb1" 
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        pygame.mouse.set_visible(False)

        self._screen = pygame.display.set_mode((480, 320), pygame.NOFRAME)
        self._screen.fill((255, 255, 255))
        self._font = pygame.font.SysFont('arial', int(480/20))
        pygame.display.update()

    def draw (self, value):
        text = self._font.render(value, True, (255, 0, 0), (255, 255, 255))
        self._screen.blit(text, (10, 10))
        self._screen.blit(text, (10, 50))
        self._screen.blit(text, (10, 90))
        pygame.display.update()

       

###############################################################################
# Exit ########################################################################
def Exit():
    """stuff to be done on exit"""
    print("Exit")
    readI2C.stop()
    readI2C.join()
    pygame.quit()
    sys.exit()

def _Exit(__s, __f):
    """exit for signal handler"""
    print("_Exit")
    Exit()


###############################################################################
###############################################################################
if __name__ == '__main__':
    signal.signal(signal.SIGTERM, _Exit)

    try:
        readI2C = ReadI2C()
        readI2C.start()

        display = Display()

        while True:
            v = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
            display.draw(v)


    except KeyboardInterrupt:
        Exit()

    except SystemExit:              # Done in signal handler (method _Exit()) #
        pass

    except:
        print(traceback.print_exc())

    finally:    # All cleanup is done in KeyboardInterrupt or signal handler. #
        pass

# eof #

