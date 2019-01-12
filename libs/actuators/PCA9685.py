# -*- coding: utf-8 -*-
###############################################################################
# PCA9685.py                                                                  #
# Communication with 16 channel PWM device PCA9685.                           #
# (c) https://github.com/thomaspfeiffer-git 2017, 2018                        #
###############################################################################
"""provides a class for handling the 16 channel PWM device PCA9685"""

# code taken and modified from
# https://github.com/adafruit/Adafruit_Python_PCA9685/blob/master/Adafruit_PCA9685/PCA9685.py
# https://github.com/voidpp/PCA9685-driver/blob/master/pca9685_driver/device.py

from i2c import I2C
import sys
import time

from Logging import Log

PCA9685_BASE_ADDRESS = 0x40 # caution: interferes with HTU21DF_BASE_ADDR

class PCA9685 (I2C):
    # Registers:
    MODE1     = 0x00
    MODE2     = 0x01
    PRE_SCALE = 0xFE

    LED0_ON_L          = 0x06
    LED0_ON_H          = 0x07
    LED0_OFF_L         = 0x08
    LED0_OFF_H         = 0x09

    # Bits:
    SLEEP     = 0x10
    ALLCALL   = 0x01
    OUTDRV    = 0x04

    MAX       = 4095
    MIN       = 0

    _first = True

    def __init__ (self, address=PCA9685_BASE_ADDRESS, frequency=100, lock=None):
        super().__init__(lock)

        self.__lastvalue_on = None
        self.__lastvalue_off = None

        self.__address = address
        if PCA9685._first:   # reset on first init
            self.all_reset()
            self.set_freq(frequency)
            PCA9685._first = False

    def __read (self, reg):
        with I2C._lock:
            return I2C._bus.read_byte_data(self.__address, reg)

    def __write (self, reg, value):
        """Write raw byte value to the specified register"""
        try:
            with I2C._lock:
                I2C._bus.write_byte_data(self.__address, reg, value)
        except:
            Log("Cannot write to i2c bus: {0[0]} {0[1]}".format(sys.exc_info()))

    def __sleep (self):
        """Send the controller to sleep"""
        self.__write(self.MODE1, self.__read(self.MODE1) | (1 << self.SLEEP))

    def __wake (self):
        """Wake up the controller"""
        self.__write(self.MODE1, self.__read(self.MODE1) & (255 - (1 << self.SLEEP)))
        time.sleep(0.005)  # wait for oscillator

    def all_reset (self):
        # self.set_all_pwm(0, 0)
        self.__write(self.MODE1, self.ALLCALL)
        self.__write(self.MODE2, self.OUTDRV)
        time.sleep(0.005)  # wait for oscillator
        self.__wake()

    def set_freq (self, freq_hz):
        prescaleval = 25000000.0    # 25MHz
        prescaleval /= 4096.0       # 12-bit
        prescaleval /= float(freq_hz)
        prescaleval -= 1.0
        prescale = int(round(prescaleval))

        self.__sleep()
        self.__write(self.PRE_SCALE, prescale)
        self.__wake()

    def set_pwm (self, channel, on, off):
        if self.__lastvalue_on != on or self.__lastvalue_off != off:
            self.__lastvalue_on  = on
            self.__lastvalue_off = off
            self.__write(self.LED0_ON_L+4*channel, on & 0xFF)
            self.__write(self.LED0_ON_H+4*channel, on >> 8)
            self.__write(self.LED0_OFF_L+4*channel, off & 0xFF)
            self.__write(self.LED0_OFF_H+4*channel, off >> 8)

# eof #

