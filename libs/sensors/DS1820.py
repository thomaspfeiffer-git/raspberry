# -*- coding: utf-8 -*-
###############################################################################################
# DS1820.py                                                                                   #
# Communication with DS1820                                                                   #
# (c) https://github.com/thomaspfeiffer-git May 2015, 2016                                    #
###############################################################################################

import re
import time

class DS1820:
   def __init__ (self, id, qvalue=None):
      self.__id        = id
      self.__qvalue    = qvalue
      self.__lastvalue = 0
   
   def __read_sensor (self):
      try:
         with open(self.__id, "r") as f:
            line = f.readline()
            if re.match(r"([0-9a-f]{2} ){9}: crc=[0-9a-f]{2} YES", line):
               line = f.readline()
               m = re.match(r"([0-9a-f]{2} ){9}t=([+-]?[0-9]+)", line)
               if m:
                  self.__lastvalue = float(m.group(2)) / 1000.0

      except IOError as e:
         print(time.strftime("%x %X"), "Error reading", self.__id, ": ", e)

      finally:
         return self.__lastvalue

   def read (self):
       value = self.__read_sensor()
       if value is not None:
           if self.__qvalue is not None:
               qvalue = "%.1f" % (value)
               self.__qvalue.value = qvalue
       return value

### eof ###

