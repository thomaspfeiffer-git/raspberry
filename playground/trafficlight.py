#!/usr/bin/python3
# -*- coding: utf-8 -*-
###############################################################################
# trafficlight.py                                                             #
# (c) https://github.com/thomaspfeiffer-git 2016                              #
###############################################################################
"""Simulates a usual traffic light (located at a usual crossroad)
   TL1: Traffic light for street #1
   TL2: Traffic light for street #2
"""

import RPi.GPIO as io
import signal
import sys
from time import sleep
import traceback


TL1_PIN_RED    = 29
TL1_PIN_ORANGE = 31
TL1_PIN_GREEN  = 33

TL2_PIN_RED    = 36
TL2_PIN_ORANGE = 38
TL2_PIN_GREEN  = 40


class Lamp (object):
    """one lamp of the traffic light (typically red, orange, or green)"""
    def __init__ (self, pin):
        self._pin = pin
        io.setup(self._pin, io.OUT)
        self.off()

    def on (self):
        """turns lamp on"""
        io.output(self._pin, io.HIGH)

    def off (self):
        """turns lamp off"""
        io.output(self._pin, io.LOW)


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
# Exit ########################################################################
def Exit():
    """stuff to be done on exit"""
    print("Exit")
    T.stop()
    io.cleanup()
    sys.exit()

def _Exit(__s, __f):
    """exit for signal handler"""
    print("_Exit")
    Exit()


###############################################################################
###############################################################################
if __name__ == '__main__':
    signal.signal(signal.SIGTERM, _Exit)
    io.setmode(io.BOARD)

    try:
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

