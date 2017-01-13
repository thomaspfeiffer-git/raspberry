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
    PRE_SCALE = 0xFE
    _first = True

    def __init__ (self, address=PCA9685_ADDRESS, lock=None):
        super().__init__(lock)
        self._address = address
        if PCA9685._first:   # reset on first init
            self.all_reset()
            PCA9685._first = False


    def sleep(self):
        """Send the controller to sleep"""
        self.write(Registers.MODE_1, self.mode_1 | (1 << Mode1.SLEEP))

    def wake(self):
        """Wake up the controller"""
        self.write(Registers.MODE_1, self.mode_1 & (255 - (1 << Mode1.SLEEP)))

    def write(self, reg, value):
        """Write raw byte value to the specified register"""
        with I2C._lock:
            I2C._bus.write_byte_data(self.__address, reg, value)

    def all_reset (self):
        pass

    def set_freq (self, freq_hz):
        pass

    def set_pwm (self, channel, on, off):
        pass



