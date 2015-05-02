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
   __target = 1023
   __actual = 1023

   def __init__(self):
      threading.Thread.__init__(self)

      # SPI (MCP3008)
      self.__adc = MCP3008(SPI_const.CS0,0)

      # Hardware PWM
      wipi.wiringPiSetupPhys()
      wipi.pinMode(12,2)

      self.running = True


   def run(self):
      while (self.running):
         self.__actual = self.__adc.read()    # TODO: setter/getter
         if (self.__actual >= 1023):
            self.__actual = 1023

         if (self.__actual > self.__target):
            self.__target += 1
         elif (self.__actual < self.__target):
            self.__target -= 1

         wipi.pwmWrite(12,1024-self.__target)
         # print("Darkness: {}/{}".format(self.__actual, self.__target))
         time.sleep(0.1)


   def stop(self):
      self.running = False

### eof ###
