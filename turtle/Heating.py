###############################################################################################
# Heating.py                                                                                  #
# Control heating                                                                             #
# (c) https://github.com/thomaspfeiffer-git May 2015                                          #
###############################################################################################

import RPi.GPIO as io
from time import time


class Heating:
   def __init__ (self, pin):
      self.__pin = pin
      self.__lastchanged = 0
      self.__status = "off"

      io.setmode(io.BOARD)
      io.setup(self.__pin,io.OUT)

   def __delayperiod (self):
      t = time()
      if (t >= self.__lastchanged + 60): 
         self.__lastchanged = t
         return True
      else:
         return False

   def cleanup (self):
      io.cleanup()

   def on (self):
      if (self.__status != "on"):
         if (self.__delayperiod()):
            io.output(self.__pin,io.HIGH)
            self.__status = "on"

   def off (self):
      if (self.__status != "off"):
         if (self.__delayperiod()):
            io.output(self.__pin,io.LOW)
            self.__status = "off"

### eof ###

