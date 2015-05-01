###############################################################################################
# MCP23017                                                                                    #
# Communication with MCP23017                                                                 #
# (c) https://github.com/thomaspfeiffer-git May 2015                                          #
###############################################################################################

import smbus
from MCP23x17 import MCP23x17

class MCP23017:
   def __init__ (self, devices):
      self.__bus = smbus.SMBus(1)
      self.devices = devices

      # Set port direction to output (0b00000000)
      for d in self.devices:
         self.send(d, MCP23x17.IODIRA, 0b00000000)
         self.send(d, MCP23x17.IODIRB, 0b00000000)

   def send(self, device, bank, pattern):
      self.__bus.write_byte_data(device,bank,pattern)

### eof ###

