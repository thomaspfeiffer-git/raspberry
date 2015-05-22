###############################################################################################
# DHT22_AM2302.py                                                                             #
# Communication with DHT22_AM2302.py                                                          #
# (c) https://github.com/thomaspfeiffer-git May 2015                                          #
###############################################################################################


import dhtreader


class DHT22_AM2302:
   def __init__ (self, pin):
      self.__pin = pin
      dhtreader.init()

   def __read_sensor (self):
      i = 1 
      while (i <= 5):
         try:
            t, h = dhtreader.read(22,self.__pin) 
         except TypeError:
            t = h = -999.99
            i += 1
            continue
         break
      return [t,h]


   def read (self):
#      sum = 0
#      for i in range(0, 3):
#         sum += self.__read_sensor()
#      return sum/3
      return self.__read_sensor()


### eof ###

