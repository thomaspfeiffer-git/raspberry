###############################################################################################
# Heating.py                                                                                  #
# Control heating                                                                             #
# (c) https://github.com/thomaspfeiffer-git May 2015                                          #
###############################################################################################

import RPi.GPIO as io
from time import time


class Heating:
   ON  = "on"
   OFF = "off" 

   def __init__ (self, pin, latency):
      self.__pin = pin
      self.__latency = latency
      self.__lastchanged = 0
      self.__status = self.OFF

      io.setmode(io.BOARD)
      io.setup(self.__pin,io.OUT)


   def __delayperiod (self):
      t = time()
      if (t >= self.__lastchanged + self.__latency): 
         self.__lastchanged = t
         return True
      else:
         return False


   def status (self):
      if (self.__status == self.ON):
         return 1
      else:
         return 0


   def cleanup (self):
      io.cleanup()


   def on (self):
      if (self.__status != self.ON):
         if (self.__delayperiod()):
            io.output(self.__pin,io.HIGH)
            self.__status = self.ON


   def off (self):
      if (self.__status != self.OFF):
         if (self.__delayperiod()):
            io.output(self.__pin,io.LOW)
            self.__status = self.OFF

### eof ###

