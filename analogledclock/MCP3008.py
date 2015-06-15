###############################################################################################
# MCP3008                                                                                     #
# Communication with MCP3008                                                                  #
# (c) https://github.com/thomaspfeiffer-git 2015                                              #
###############################################################################################

import spidev

class MCP3008:
   def __init__(self, cs, channel, lock):
      self.__cs      = cs
      self.__channel = channel
      self.__lock    = lock

      self.__spi = spidev.SpiDev()
      self.__spi.open(0,self.__cs)
 

   def read(self):
      with self.__lock:
         adc = self.__spi.xfer2([1,(8+self.__channel)<<4,0])

      data = ((adc[1]&3) << 8) + adc[2]
      return data

   def close(self)
      self.__spi.close()

### eof ###

