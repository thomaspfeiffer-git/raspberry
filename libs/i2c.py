# -*- coding: utf-8 -*-
################################################################################
# i2c.py                                                                       #
# (c) https://github.com/thomaspfeiffer-git 2016                               #
################################################################################
"""provides a single instance for an i2c bus"""

import smbus
from threading import Lock

class I2C (object):
    _bus  = None
    _lock = None
    
    def __init__ (self, lock=None):
        if I2C._bus is None:
            I2C._bus  = smbus.SMBus(1)

        if I2C._lock is None:
            if lock is None:
                I2C._lock = Lock()
            else:
                I2C._lock = lock
        else:
            if lock is not None:
                raise ValueError("Lock already set!")

# eof #
