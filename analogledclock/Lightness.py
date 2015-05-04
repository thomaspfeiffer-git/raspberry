###############################################################################################
# Lightness.py                                                                                #
# Threaded class for control of lightness of LEDs                                             #
# (c) https://github.com/thomaspfeiffer-git May 2015                                          #
###############################################################################################

import time
import threading
import wiringpi2 as wipi

from SPI_const import SPI_const
from MCP3008   import MCP3008


class Value (object):
   def __init__(self, v):
      self.value = v

   @property
   def value(self):
      return self.__value

   @value.setter
   def value(self,v):
      v = int(v)
      if (v >= 1023):
         self.__value = 1023
      elif (v <= 0):
         self.__value = 0
      else:
         self.__value = v

   def __add__(self, other):
      if not isinstance(other, Value):
         other = Value(other)
      return Value(self.value + other.value)

   def __sub__(self, other):
      if not isinstance(other, Value):
         other = Value(other)
      return Value(self.value - other.value)

   def __lt__(self, other):
      if not isinstance(other, Value):
         other = Value(other)
      return self.value < other.value

   def __gt__(self, other):
      if not isinstance(other, Value):
         other = Value(other)
      return self.value > other.value

   def __str__(self):
      return str(self.value)


class Lightness (threading.Thread):
   def __init__(self):
      threading.Thread.__init__(self)

      # SPI (MCP3008)
      self.__adc = MCP3008(SPI_const.CS0,0)

      # Hardware PWM
      wipi.wiringPiSetupPhys()
      wipi.pinMode(12,2)

      self.running = True


   def run(self):
      target = Value(102)
      while (self.running):
         actual = Value(self.__adc.read())

         if (actual > target+25):
            target += 25
         elif (actual < target-25):
            target -= 25
         if (actual > target+10):
            target += 10
         elif (actual < target-10):
            target -= 10
         elif (actual > target):
            target += 1
         elif (actual < target):
            target -= 1

         wipi.pwmWrite(12,1024-target.value)
         print("Lightness: {}/{}".format(actual,target))
         time.sleep(0.1)


   def stop(self):
      self.running = False

### eof ###

