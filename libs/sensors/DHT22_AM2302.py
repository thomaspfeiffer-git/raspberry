# -*- coding: utf-8 -*-
###############################################################################################
# DHT22_AM2302.py                                                                             #
# Communication with DHT22_AM2302.py                                                          #
# (c) https://github.com/thomaspfeiffer-git May 2015, 2016, 2023                              #
###############################################################################################

import Adafruit_DHT
import numpy as np


class DHT22_AM2302:
   ERROR = -999.99

   def __init__ (self, pin):
      self.__pin = pin

   def __read_sensor (self):
      i = 1
      while (i <= 5):
         try:
            h, t = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, self.__pin) # BCM/GPIO
            if (h is None) or (t is None):
               t = h = self.ERROR
               i += 1
               continue
         except TypeError:
            t = h = self.ERROR
            i += 1
            continue
         break
      return [t,h]

   def read (self):
      t = [self.ERROR]
      h = [self.ERROR]
      for i in range(0, 10):
         __t, __h = self.__read_sensor()
         if (__t == self.ERROR):
            continue
         t.append(__t)
         h.append(__h)

      t.sort()
      h.sort()

      t_avg = np.mean(t[int(len(t)/3):int(len(t)/3)*2])
      h_avg = np.mean(h[int(len(h)/3):int(len(h)/3)*2])

      return [t_avg, h_avg]

### eof ###

