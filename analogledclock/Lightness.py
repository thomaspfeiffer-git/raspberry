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
      # print "Setter v:", v
      if (v >= 1023):
         self.__value = 1023
      elif (v <= 0):
         self.__value = 0
      else:
         self.__value = int(v)


   def __add__(self, other):
      if not isinstance(other, Value):
         other = Value(other)
      return Value(self.value + other.value)

   def __sub__(self, other):
      if not isinstance(other, Value):
         other = Value(other)
      return Value(self.value - other.value)



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
      target = Value(1024)
      while (self.running):
         actual = Value(self.__adc.read())

         if (actual.value > target.value+25):
            target += 25
         elif (actual.value < target.value-25):
            target -= 25
         if (actual.value > target.value+10):
            target += 10
         elif (actual.value < target.value-10):
            target -= 10
         elif (actual.value > target.value):
            target += 1
         elif (actual.value < target.value):
            target -= 1

         wipi.pwmWrite(12,1024-target.value)
         print("Lightness: {}/{}".format(actual.value,target.value))
         time.sleep(0.1)


   def stop(self):
      self.running = False

### eof ###

