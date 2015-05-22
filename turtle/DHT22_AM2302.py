###############################################################################################
# DHT22_AM2302.py                                                                             #
# Communication with DHT22_AM2302.py                                                          #
# (c) https://github.com/thomaspfeiffer-git May 2015                                          #
###############################################################################################

import dhtreader

class DHT22_AM2302:
   __ERROR = -999.99
   def __init__ (self, pin):
      self.__pin = pin
      dhtreader.init()

   def __read_sensor (self):
      i = 1 
      while (i <= 5):
         try:
            t, h = dhtreader.read(22,self.__pin) 
         except TypeError:
            t = h = __ERROR
            i += 1
            continue
         break
      return [t,h]

   def read (self):
      sum_t = sum_h = 0
      for i in range(0, 3):
         t, h = self.__read_sensor()
         sum_t += t
         sum_h += h
         # TODO: Better handling for ERROR needed
      return [sum_t/3, sum_h/3]

### eof ###

