# -*- coding: utf-8 -*-
###############################################################################################
# DS1820.py                                                                                   #
# Communication with DS1820                                                                   #
# (c) https://github.com/thomaspfeiffer-git May 2015                                          #
###############################################################################################

import re

class DS1820:
   def __init__ (self, id, qvalue=None):
      self.__id     = id
      self.__qvalue = qvalue
   
   def __read_sensor (self):
     value = 99 # TODO: improve error handling
     try:
       f = open(self.__id, "r")
       line = f.readline()
       if re.match(r"([0-9a-f]{2} ){9}: crc=[0-9a-f]{2} YES", line):
         line = f.readline()
         m = re.match(r"([0-9a-f]{2} ){9}t=([+-]?[0-9]+)", line)
         if m:
           value = float(m.group(2)) / 1000.0
       f.close()
     except (IOError), e:
       print time.strftime("%x %X"), "Error reading", self.__id, ": ", e
     return value

   def read (self):
      sum = 0
      for i in range(0, 3): # TODO: improve error handling
         sum += self.__read_sensor()

      sum = sum/3.0

      if self.__qvalue is not None:
          value = "%.1f %s" % (sum, u'°C')
          value = value.replace('.', ',')   # TODO: move to SensorValue.value()
          self.__qvalue.value = value

      return sum

### eof ###

