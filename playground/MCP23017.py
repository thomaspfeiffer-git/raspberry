################################################################################
# MCP23017                                                                     #
# Communication with MCP23017                                                  #
# (c) https://github.com/thomaspfeiffer-git 2015, 2016                         #
################################################################################
"""control component MCP23017"""

from time import localtime

from i2c import I2C
from MCP23x17 import MCP23x17

class MCP23017 (I2C):
    """control component MCP23017"""
    def __init__ (self, address, lock=None):
        super().__init__(lock)
        self._address = address

        # Set port direction to output (0b00000000)
        self.send(MCP23x17.IODIRA, 0b00000000)
        self.send(MCP23x17.IODIRB, 0b00000000)

    def send (self, bank, pattern):
        """send pattern to bank of device"""
        i = 0
        while (i < 3):
            try:
                with I2C._lock:
                    I2C._bus.write_byte_data(self._address, bank, pattern)
            except IOError:
                print(localtime()[3:6], "Device:", hex(device), "Bank:", hex(bank), "Pattern:", bin(pattern))
                i += 1
                print("Retry: %i" % i)
                continue
            break

    def read (self):
        raise NotImplementedError

### eof ###

