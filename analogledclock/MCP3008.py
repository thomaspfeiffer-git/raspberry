###############################################################################################
# MCP3008                                                                                     #
# Communication with MCP3008                                                                  #
# (c) https://github.com/thomaspfeiffer-git 2015                                              #
###############################################################################################

import spidev

class MCP3008_xfer:
   def __init__(self, cs, channel, lock):
      self.channel = channel
      # self.cs = 0 if (cs == SPI_const.CS0) else 1      
      self.cs      = cs
      self.lock    = lock

      self.spi = spidev.SpiDev()
      self.spi.open(0,0)  # TODO: cs
 

   def read(self):
      with self.lock:
         adc = self.spi.xfer2([1,(8+self.channel)<<4,0])

      data = ((adc[1]&3) << 8) + adc[2]
      return data

### eof ###

