################################################################################
# MCP3008                                                                      #
# Communication with MCP3008                                                   #
# (c) https://github.com/thomaspfeiffer-git 2015                               #
################################################################################
"""communication with MCP3008 including a lock in case of more than one
   chip is using the SPI bus"""

import spidev

class MCP3008:
    """class for communication with MCP3008"""
    def __init__(self, chipselect, channel, lock):
        self.__cs      = chipselect
        self.__channel = channel
        self.__lock    = lock

        self.__spi = spidev.SpiDev()
        self.__spi.open(0, self.__cs)
 

    def read(self):
        """read data from MCP3008"""
        with self.__lock:
            adc = self.__spi.xfer2([1, (8+self.__channel)<<4, 0])

        data = ((adc[1]&3) << 8) + adc[2]
        return data

    def close(self):
        """close SPI"""
        self.__spi.close()

### eof ###

