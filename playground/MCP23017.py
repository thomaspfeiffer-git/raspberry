################################################################################
# MCP23017                                                                     #
# Communication with MCP23017                                                  #
# Parts of this source code come from                                          #
# https://github.com/BLavery/lib_mcp23017/blob/master/lib_mcp23017.py          #
# (c) https://github.com/thomaspfeiffer-git 2015, 2016                         #
################################################################################
"""control component MCP23017"""

from time import localtime

from i2c import I2C
from MCP23x17 import MCP23x17

class MCP23017 (I2C):
    """control component MCP23017"""
    """ioA, ioB: 8 bits, 0: port is output
                         1: port is input"""
    def __init__ (self, address, ioA, ioB, lock=None):
        super().__init__(lock)
        self._address = address

        # Set port directions
        self.send(MCP23x17.IODIRA, ioA)
        self.send(MCP23x17.IODIRB, ioB)

        # Set pullup resistors
        self.send(MCP23x17.GPPUA, ioA)
        self.send(MCP23x17.GPPUB, ioB)

    @staticmethod
    def _BV(x):
        return 1<<x

    @staticmethod
    def _PB(bit):
        port = (bit >> 3) + MCP23x17.GPIOA 
        bit &= 7           # = always 0-7
        return port, bit 

    def send (self, bank, pattern):
        """send pattern to bank of device"""
        # TODO: Test what happens if writing to a bank with 
        # mixed input/output bits.
        # TODO: switch to bits/patterns without dedicated banks
        i = 0
        while (i < 3):
            try:
                with I2C._lock:
                    I2C._bus.write_byte_data(self._address, bank, pattern)
                    break
            except IOError:
                print(localtime()[3:6], "Device:", hex(device), "Bank:", hex(bank), "Pattern:", bin(pattern))
                i += 1
                print("Retry: %i" % i)
                continue

    def output (self, bit, value):
        port, bit = self._PB(bit)
        # ...

    def read (self, bit):
        """reads bit; bit is int 0..15"""
        port, bit = self._PB(bit)
        try:
            with I2C._lock:
                return (I2C._bus.read_byte_data(self._address, port) & self._BV(bit)) == 0
        except IOError:
            print("Could not read MCP23017 device at address", self._address)

### eof ###

