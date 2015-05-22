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

      io.setmode(io.BOARD)
      io.setup(self.__pin,io.OUT)

   def __delayperiod (self):
      t = time()
      print t
      if (t >= self.__lastchanged + 100): 
         self.__lastchanged = t
         return True
      else:
         return False

   def cleanup (self):
      io.cleanup()

   def on (self):
      print "try on"
      if (self.__delayperiod()):
         io.output(self.__pin,io.HIGH)
         print "on"

   def off (self):
      print "try off"
      if (self.__delayperiod()):
         io.output(self.__pin,io.LOW)
         print "off"



### eof ###

