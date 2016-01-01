################################################################################
# MCP23S17                                                                     #
# Communication with MCP23S17                                                  #
# (c) https://github.com/thomaspfeiffer-git 2015                               #
################################################################################
"""control component MCP23S17"""

import spidev

from MCP23x17 import MCP23x17


class MCP23S17:
    """control component MCP23S17"""
    SLAVE_ADDR_BASE = 0x40
    SLAVE_WRITE     = 0x00
    SLAVE_READ      = 0x01

    def send (self, device, register, data):
        """send data to device"""
        d = device << 1
        with self.__lock:
            self.__spi.xfer2([d|self.SLAVE_ADDR_BASE|self.SLAVE_WRITE, register, data])


    def __init__ (self, cs, devices, lock):
        self.__cs      = cs
        self.__devices = devices
        self.__lock    = lock

        self.__spi = spidev.SpiDev()
        self.__spi.open(0, self.__cs)

        # MCP23S17 needs hardware addressing explicitly enabled.
        for d in self.__devices:
            self.send(d, MCP23x17.IOCONA, MCP23x17.HAEN)
            self.send(d, MCP23x17.IOCONB, MCP23x17.HAEN)

        # Set port direction to output (0b00000000)
        for d in self.__devices:
            self.send(d, MCP23x17.IODIRA, 0x00)
            self.send(d, MCP23x17.IODIRB, 0x00)


    def close (self):
        """close spi bus"""
        self.__spi.close()


### eof ###

