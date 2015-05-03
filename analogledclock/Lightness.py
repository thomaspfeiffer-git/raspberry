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


class Lightness (threading.Thread):
   def __init__(self):
      threading.Thread.__init__(self)

      # SPI (MCP3008)
      self.__adc = MCP3008(SPI_const.CS0,0)

      # Hardware PWM
      wipi.wiringPiSetupPhys()
      wipi.pinMode(12,2)

      self.running = True


   def __boundaries(value):
      if (value >= 1023):
         return 1023
      elif (value <= 0):
         return 0
      else:
         return value


   @property
   def actual(self):
      return self.__actual

   @actual.setter
   def actual(self, value):
      self.__actual == __boundaries(value)


   @property
   def target(self):
      return self.__target

   @target.setter
   def setter(self,value):      
      self.__target = __boundaries(value)


   def run(self):
      target = 1024
      while (self.running):
         actual = self.__adc.read() 

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

         target = (target // 10) * 10
         wipi.pwmWrite(12,1024-target)
         # print("Lightness: {}/{}".format(actual,target))
         time.sleep(0.1)


   def stop(self):
      self.running = False

### eof ###

