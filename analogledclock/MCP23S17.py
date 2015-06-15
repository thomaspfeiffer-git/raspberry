###############################################################################################
# MCP23017                                                                                    #
# Communication with MCP23S17                                                                 #
# (c) https://github.com/thomaspfeiffer-git 2015                                              #
###############################################################################################

import spidev

from MCP23x17 import MCP23x17


class MCP23S17:
   SLAVE_ADDR_BASE = 0x40
   SLAVE_WRITE     = 0x00
   SLAVE_READ      = 0x01

   def send (self, device, register, data):
      d = device << 1
      with self.lock:
         self.spi.xfer2([d|self.SLAVE_ADDR_BASE|self.SLAVE_WRITE,register,data])


   def __init__ (self, cs, devices, lock):
      self.cs      = cs
      self.devices = devices
      self.lock    = lock

      self.spi = spidev.SpiDev()
      self.spi.open(0,self.cs)

      # MCP23S17 needs hardware addressing explicitly enabled.
      for d in self.devices:
         self.send(d, MCP23x17.IOCONA, MCP23x17.HAEN)
         self.send(d, MCP23x17.IOCONB, MCP23x17.HAEN)

      # Set port direction to output (0b00000000)
      for d in self.devices:
         self.send(d, MCP23x17.IODIRA, 0x00)
         self.send(d, MCP23x17.IODIRB, 0x00)


   def close (self):
      self.spi.close()


### eof ###

