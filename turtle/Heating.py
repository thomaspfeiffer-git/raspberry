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
   __instances = 0

   def __off (self):
      io.output(self.__pin,io.LOW)
      self.__status = self.OFF  


   def __init__ (self, pin, latency, dryRun=False):
      Heating.__instances += 1
      self.__pin     = pin
      self.__latency = latency
      self.__dryRun  = dryRun
      self.__lastchanged = 0
      self.__status  = self.OFF

      io.setmode(io.BOARD)
      io.setup(self.__pin,io.OUT)
      self.__off()


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
      print "Heatlamp.cleanup()"
      self.__off()
      if Heating.__instances == 1:
         io.cleanup()
      else:
         Heating.__instances -= 1


   def on (self):
      if (self.__status != self.ON):
         if (self.__delayperiod()):
            if (self.__dryRun):
               print("Dry run: {}".format(self.ON))
            else:
               io.output(self.__pin,io.HIGH)
            self.__status = self.ON


   def off (self):
      if (self.__status != self.OFF):
         if (self.__delayperiod()):
            self.__off()

### eof ###

