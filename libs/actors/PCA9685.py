# -*- coding: utf-8 -*-
###############################################################################
# PCA9685.py                                                                  #
# Communication with 16 channel PWM device PCA9685.                           #
# (c) https://github.com/thomaspfeiffer-git 2017                              #
###############################################################################
"""provides a class for handling the 16 channel PWM device PCA9685"""

# code taken and modified from
# https://github.com/adafruit/Adafruit_Python_PCA9685/blob/master/Adafruit_PCA9685/PCA9685.py
# https://github.com/voidpp/PCA9685-driver/blob/master/pca9685_driver/device.py


from i2c import I2C


PCA9685_ADDRESS = 0x40


class PCA9685 (I2C):
    # Registers:
    MODE1     = 0x00
    MODE2     = 0x01
    PRE_SCALE = 0xFE

    # Bits:
    SLEEP     = 0x10

    _first = True

    def __init__ (self, address=PCA9685_ADDRESS, lock=None):
        super().__init__(lock)

        self._address = address
        if PCA9685._first:   # reset on first init
            self.all_reset()
            PCA9685._first = False

    def __read (self, reg):
        return I2C._bus.read_byte_data(self.__address, reg)

    def __write (self, reg, value):
        """Write raw byte value to the specified register"""
        with I2C._lock:
            I2C._bus.write_byte_data(self.__address, reg, value)

    def __sleep (self):
        """Send the controller to sleep"""
        self.__write(MODE1, self.__read(MODE1) | (1 << SLEEP))

    def __wake (self):
        """Wake up the controller"""
        self.__write(MODE1, self.__read(MODE1) & (255 - (1 << SLEEP)))

    def all_reset (self):
        pass

    def set_freq (self, freq_hz):
        pass

    def set_pwm (self, channel, on, off):
        pass

# eof #

