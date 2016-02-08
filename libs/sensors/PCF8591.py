# -*- coding: utf-8 -*-
################################################################################
# PCF8591.py                                                                   #
# (c) https://github.com/thomaspfeiffer-git 2016                               #
################################################################################
"""controls A/D converter PCF8591"""

from i2c import I2C

class PCF8591 (I2C):
    def __init__ (self, address, lock=None):
        super().__init__(lock)
        self._address = address

    def read (self, channel=0):
        with I2C._lock:
            I2C._bus.write_byte(self._address, 0x40|channel)
            ack = I2C._bus.read_byte(self._address)  # don't use ack
            return I2C._bus.read_byte(self._address) 

    def write (self, value):
        raise NotImplementedError

# eof #

