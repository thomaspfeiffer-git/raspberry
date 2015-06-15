###############################################################################################
# DHT22_AM2302.py                                                                             #
# Communication with DHT22_AM2302.py                                                          #
# (c) https://github.com/thomaspfeiffer-git May 2015                                          #
###############################################################################################

import dhtreader
import numpy as np

class DHT22_AM2302:
   ERROR = -999.99

   def __init__ (self, pin):
      self.__pin = pin
      dhtreader.init()

   def __read_sensor (self):
      i = 1 
      while (i <= 5):
         try:
            t, h = dhtreader.read(22,self.__pin) 
         except TypeError:
            t = h = self.ERROR
            i += 1
            continue
         break
      return [t,h]

   def read (self):
      t = []
      h = []
      count = 0
      for i in range(0, 10):
         __t, __h = self.__read_sensor()
         if (__t == self.ERROR):
            continue
         t.append(__t)
         h.append(__h)
         count += 1

      t.sort()
      h.sort()

      t_avg = np.mean(t[int(count/3):int(count/3)*2])
      h_avg = np.mean(h[int(count/3):int(count/3)*2])
      return [t_avg, h_avg]

### eof ###

