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
      self.__id     = id
      self.__qvalue = qvalue
   
   def __read_sensor (self):
      try:
         with open(self.__id, "r") as f:
            line = f.readline()
            print "DS1820, Line #1:", time.strftime("%x %X"), "---", line
            if re.match(r"([0-9a-f]{2} ){9}: crc=[0-9a-f]{2} YES", line):
               line = f.readline()
               print "DS1820, Line #2:", time.strftime("%x %X"), "---", line
               m = re.match(r"([0-9a-f]{2} ){9}t=([+-]?[0-9]+)", line)
               if m:
                  return float(m.group(2)) / 1000.0

      except (IOError), e:
         print time.strftime("%x %X"), "Error reading", self.__id, ": ", e

      return None


   def read (self):
      sum = 0.0
      no_reads = 0
      for i in range(3):
         value = self.__read_sensor()
         print "DS1820, try", i, ":", value
         if value:
            sum += value
            no_reads += 1

      if no_reads == 0:
          return None
      else:
          sum = sum/no_reads
          print "DS1820, sum", ":", sum

          if self.__qvalue is not None:
              value = "%.1f" % (sum)
              self.__qvalue.value = value

          return sum

### eof ###

