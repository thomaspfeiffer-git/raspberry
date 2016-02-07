#!/usr/bin/python3
# -*- coding: utf-8 -*-
################################################################################
# PCF8591.py                                                                   #
# (c) https://github.com/thomaspfeiffer-git 2016                               #
################################################################################
"""controls A/D converter PCF8591"""




import smbus
from threading import Lock
import time


class I2C (object):
    _bus  = None
    _lock = None
    
    def __init__ (self, lock=None):
        self._bus  = smbus.SMBus(1)
        if self._lock is None:
            if lock is None:
                self._lock = Lock()
            else:
                self._lock = lock
        else:
            if lock is not None:
                raise ValueError("Lock already set!")


# Taken from https://github.com/jacotronix/net.jacotronix.python.PCF8591P/blob/master/PCF8591P/PCF8591P.py
class PCF8591 (I2C):
    def __init__ (self, address, lock=None):
        super().__init__(lock)
        self._address = address

    def readchannel (self, channel=0):
        with self._lock:
            self._bus.write_byte(self._address, 0x40|channel)
            ack = self._bus.read_byte(self._address)  # don't use ack
            return self._bus.read_byte(self._address) 


if __name__ == '__main__':
    adc = PCF8591(0x48)

    while True:
        result = adc.readchannel(0)
        print("Result 0: %s" % result)
        result = adc.readchannel(1)
        print("Result 1: %s" % result)
        result = adc.readchannel(2)
        print("Result 2: %s" % result)
        result = adc.readchannel(3)
        print("Result 3: %s" % result)
        print("--------------------")
        time.sleep(0.5)



 
