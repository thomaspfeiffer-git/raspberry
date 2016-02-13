#!/usr/bin/python3
# -*- coding: utf-8 -*-
###############################################################################
# trafficlight.py                                                             #
# (c) https://github.com/thomaspfeiffer-git 2016                              #
###############################################################################
"""Simulates a usual traffic light (located at a usual crossroad)
   TL1: Traffic light for street #1
   TL2: Traffic light for street #2
   Lightness of lamps is controlled by PWM using an LDR.
   Additionally the values of the LDR are written to the display.
   Goal: Test if a Tontec display works properly when an I2C bus is used
   as well (for an MCP23017 and a PCF8591).
"""

import os
import pygame
import signal
import sys
import threading
from time import sleep
import traceback


sys.path.append('../libs')
sys.path.append('../libs/sensors')

from MCP23x17 import MCP23x17
from MCP23017 import MCP23017
from PCF8591  import PCF8591
from pwm      import PWM


TL1_PIN_RED    = 0b10000000
TL1_PIN_ORANGE = 0b01000000
TL1_PIN_GREEN  = 0b00100000

TL2_PIN_RED    = 0b00010000
TL2_PIN_ORANGE = 0b00001000
TL2_PIN_GREEN  = 0b00000100


###############################################################################
class Lamp (object):
    """one lamp of the traffic light (typically red, orange, or green)"""
    _device  = MCP23017(0x20)
    _pattern = 0b00000000

    def __init__ (self, pin):
        self._pin = pin
        self.off()

    def on (self):
        """turns lamp on"""
        Lamp._pattern |= self._pin
        self._write()

    def off (self):
        """turns lamp off"""
        Lamp._pattern &= ~self._pin
        self._write()

    def _write (self):
        Lamp._device.send(MCP23x17.OLATA, Lamp._pattern)


###############################################################################
class Trafficlight (object):
    """one traffic light built of three lamps (red, orange, green)"""
    def __init__ (self, pin_red, pin_orange, pin_green):
        self.red    = Lamp(pin_red)
        self.orange = Lamp(pin_orange)
        self.green  = Lamp(pin_green)
        self._lamps = [self.red, self.orange, self.green]

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

    def __init__ (self, tl1, tl2):
        self._tl1 = tl1
        self._tl2 = tl2
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
           checks self.__running and exits if False"""
        for _ in range(int(time*10.0)):
            sleep(0.1)
            if not self.__running:
                break

    def _go_red (self, trafficlight):  
        """switches trafficlight to red"""
        self._blink(trafficlight.green)
        trafficlight.orange.on()
        self.__sleep(self.TIME_ORANGE)
        trafficlight.orange.off()
        trafficlight.red.on()

    def _go_green (self, trafficlight):
        """switches trafficlight to green"""
        trafficlight.orange.on()
        self.__sleep(self.TIME_ORANGE)
        trafficlight.red.off()
        trafficlight.orange.off()
        trafficlight.green.on()

    def run (self):
        """runs the thread
           switches tl1 to red and green and 
           switches tl2 to green and red"""
        while self.__running:
            self._go_red(self._tl1)
            self._go_green(self._tl2)
            self.__sleep(self.TIME_RED)
            self._go_red(self._tl2)
            self._go_green(self._tl1)
            self.__sleep(self.TIME_GREEN)

        for trafficlight in (self._tl1, self._tl2):
            trafficlight.all_off()

    def stop (self):
        """shall be called in order to stop the thread"""
        self.__running = False


###############################################################################
class Lightness (threading.Thread):
    def __init__ (self):
        threading.Thread.__init__(self)
        self._adc = PCF8591(0x48)
        self._pwm = PWM()

        self.__running = True

    def run (self):
        while self.__running:
            v = 1024 - (self._adc.read() * 4) 
            if v > 1020:
               v = 1020
            # print("Value ADC: %i" % v) 
            self._pwm.control(v)
            sleep(0.5)

    def stop (self):
        self.__running = False

    def getadc (self):
        return self._adc.read()


###############################################################################
class Display (threading.Thread):
    def __init__ (self, getadc):
        threading.Thread.__init__(self)
        self._getadc = getadc

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
        value = "%s     " % str(self._getadc())
        text = self.font.render(value, True, (255, 0, 0), (255, 255, 255))
        self.screen.blit(text, (10, 10))
        pygame.display.update()


###############################################################################
# Exit ########################################################################
def Exit():
    """stuff to be done on exit"""
    print("Exit")
    display.stop()
    display.join()
    lightness.stop()
    lightness.join()
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
        lightness = Lightness()
        lightness.start()

        display = Display(lightness.getadc)
        display.start()

        T1 = Trafficlight(TL1_PIN_RED, TL1_PIN_ORANGE, TL1_PIN_GREEN)
        T2 = Trafficlight(TL2_PIN_RED, TL2_PIN_ORANGE, TL2_PIN_GREEN)
        T = Trafficlights(T1, T2)
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

