#!/usr/bin/python3
# -*- coding: utf-8 -*-
###############################################################################
# trafficlight.py                                                             #
# (c) https://github.com/thomaspfeiffer-git 2016                              #
###############################################################################
"""Simulates a usual traffic light (located at a usual crossroad)
   TL1: Traffic light for cars for street #1
   TL2: Traffic light for cars for street #2
   TL3: Traffic light for pedestrians street #1
   TL4: Traffic light for pedestrians street #2
   Goal: Test if a Tontec display works properly when an I2C bus is used
   as well (for an MCP23017)
"""

import os
import pygame
import RPi.GPIO as io
import signal
import sys
import threading
from time import sleep
import traceback


sys.path.append('../libs')
sys.path.append('../libs/sensors')

from MCP23x17 import MCP23x17
from MCP23017 import MCP23017


TL1_PIN_RED    = 0b10000000
TL1_PIN_ORANGE = 0b01000000
TL1_PIN_GREEN  = 0b00100000

TL2_PIN_RED    = 0b00010000
TL2_PIN_ORANGE = 0b00001000
TL2_PIN_GREEN  = 0b00000100

TL3_PIN_RED    = 0b00000010
TL3_PIN_GREEN  = 0b00000001


device = MCP23017(0x20, 0b00000000, 0b11000000)


###############################################################################
class Lamp (object):
    """one lamp of the traffic light (typically red, orange, or green)"""
    _pattern = 0b00000000

    def __init__ (self, pin):
        self._pin = pin
        self.off()

    def on (self):
        """turns lamp on"""
        Lamp._pattern |= self._pin
        Lamp._write()

    def off (self):
        """turns lamp off"""
        Lamp._pattern &= ~self._pin
        Lamp._write()

    @staticmethod
    def _write():
        device.send(MCP23x17.OLATA, Lamp._pattern)


###############################################################################
class Trafficlight (object):
    """one traffic light built of three lamps (red, orange, green)"""
    def __init__ (self, pin_red, pin_green, pin_orange=None):
        self.red    = Lamp(pin_red)
        self.green  = Lamp(pin_green)
        self._lamps = [self.red, self.green]
        if pin_orange:
            self.orange = Lamp(pin_orange)
            self._lamps.append(self.orange)

    def all_on (self):
        """switch all lamps on (just for testing purpose)"""
        for lamp in self._lamps:
            lamp.on()

    def all_off (self):
        """switch all lamps off;
           needed at start of program and for cleanup"""
        for lamp in self._lamps:
            lamp.off()


###############################################################################
class Trafficlights (object):
    """control of complete traffic light"""
    TIME_RED    = 10 
    TIME_GREEN  = 10
    TIME_ORANGE =  2

    def __init__ (self, tl1, tl2, tl3):
        self._tl1      = tl1  # for cars
        self._tl2      = tl2
        self._tl3      = tl3  # for pedestrians
        self.__running = True

    def _blink (self, lamp, count=5):
        """flashes a lamp <count> times with a frequency of 1 Hz"""
        for _ in range(count):
            self.__sleep(0.5)
            lamp.on()
            self.__sleep(0.5)
            lamp.off()
            if not self.__running:
                break

    def __sleep (self, time):
        """sleeps n seconds
           - pauses traffic light if sensor is active
           - checks self.__running and exits if False"""
        i = 0.0
        while (i <= time*10.0):
            sleep(0.1)
            if not device.read(bit=6):
                i += 1.0
            if not self.__running:
                break

    def _go_red_cars (self, trafficlight):  
        """switches trafficlight for cars to red"""
        self._blink(trafficlight.green)
        trafficlight.orange.on()
        self.__sleep(self.TIME_ORANGE)
        trafficlight.orange.off()
        trafficlight.red.on()

    def _go_red_walk (self, trafficlight):
        """switches trafficlight for pedestrians to red"""
        self._blink(trafficlight.green)
        trafficlight.red.on()

    def _go_green_cars (self, trafficlight):
        """switches trafficlight for cars to green"""
        trafficlight.orange.on()
        self.__sleep(self.TIME_ORANGE)
        trafficlight.red.off()
        trafficlight.orange.off()
        trafficlight.green.on()

    def _go_green_walk (self, trafficlight):
        """switches trafficlight for pedestrians to green"""
        trafficlight.red.off()
        trafficlight.green.on()

    def run (self):
        """runs the thread
           switches tl1 to red and green and 
           switches tl2 to green and red"""
        while self.__running:
            self._go_red_walk(self._tl3)
            self._go_red_cars(self._tl1)
            self._go_green_cars(self._tl2)
            self.__sleep(self.TIME_RED)
            self._go_red_cars(self._tl2)
            self._go_green_cars(self._tl1)
            self._go_green_walk(self._tl3)
            self.__sleep(self.TIME_GREEN)

        for trafficlight in (self._tl1, self._tl2):
            trafficlight.all_off()

    def stop (self):
        """shall be called in order to stop the thread"""
        self.__running = False


###############################################################################
class Display (threading.Thread):
    i = 0

    def __init__ (self):
        threading.Thread.__init__(self)

        os.environ["SDL_FBDEV"] = "/dev/fb1" 
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        pygame.mouse.set_visible(False)

        self.screen = pygame.display.set_mode((480, 320), pygame.NOFRAME)
        self.screen.fill((255, 255, 255))
        self.font = pygame.font.SysFont('arial', int(480/2))
        pygame.display.update()

        self.__running = True

    def run (self):
        while self.__running:
            self.draw()
            sleep(0.5)
      
    def stop (self):
        self.__running = False      

    def draw (self):
        Display.i += 1
        if Display.i >= 999:
            Display.i = 0
        value = "%s     " % str(Display.i)

        text = self.font.render(value, True, (255, 0, 0), (255, 255, 255))
        self.screen.blit(text, (10, 10))
        pygame.display.update()


###############################################################################
# Exit ########################################################################
def Exit():
    """stuff to be done on exit"""
    print("Exit")
    T.stop()
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
        display = Display()
        display.start()

        T1 = Trafficlight(TL1_PIN_RED, TL1_PIN_GREEN, TL1_PIN_ORANGE)
        T2 = Trafficlight(TL2_PIN_RED, TL2_PIN_GREEN, TL2_PIN_ORANGE)
        T3 = Trafficlight(TL3_PIN_RED, TL3_PIN_GREEN)
        T = Trafficlights(T1, T2, T3)
        T.run()

    except KeyboardInterrupt:
        Exit()

    except SystemExit:              # Done in signal handler (method _Exit()) #
        pass

    except:
        print(traceback.print_exc())

    finally:    # All cleanup is done in KeyboardInterrupt or signal handler. #
        pass

# eof #

