################################################################################
# MCP23017                                                                     #
# Communication with MCP23017                                                  #
# (c) https://github.com/thomaspfeiffer-git May 2015                           #
################################################################################
"""control component MCP23017"""

import smbus
from time import localtime

from MCP23x17 import MCP23x17

class MCP23017:
    """control component MCP23017"""
    def __init__ (self, devices):
        self.__bus = smbus.SMBus(1)
        self.__devices = devices

        # Set port direction to output (0b00000000)
        for d in self.__devices:
            self.send(d, MCP23x17.IODIRA, 0b00000000)
            self.send(d, MCP23x17.IODIRB, 0b00000000)

    def send(self, device, bank, pattern):
        """send pattern to bank of device"""
        i = 0
        while (i < 3):
            try:
                self.__bus.write_byte_data(device, bank, pattern)
            except IOError:
                print localtime()[3:6], "Device:", hex(device), "Bank:", hex(bank), "Pattern:", bin(pattern)
                i += 1
                print "Retry:", i
                continue
            break

### eof ###

