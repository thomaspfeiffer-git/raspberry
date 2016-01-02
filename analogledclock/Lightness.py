################################################################################
# Lightness.py                                                                 #
# Threaded class for control of lightness of LEDs                              #
# (c) https://github.com/thomaspfeiffer-git May 2015                           #
################################################################################
"""controls lightness of LEDs via PWM"""

from collections import deque
import time
import threading
import wiringpi2 as wipi

from SPI_const import SPI_const
from MCP3008   import MCP3008


class Value (object):
    """provides an integer class for numbers in range 0..1023"""
    @property
    def value(self):
        """getter for value"""
        return self.__value

    @value.setter
    def value(self, v):
        """setter and validator for value"""
        v = int(v)
        if (v >= 1023):
            self.__value = 1023
        elif (v <= 0):
            self.__value = 0
        else:
            self.__value = v

    def __init__(self, v):
        self.value = v

    def __add__(self, other):
        if not isinstance(other, Value):
            other = Value(other)
        return Value(self.value + other.value)

    def __radd__(self, other):
        return Value(other + self.value)

    def __sub__(self, other):
        if not isinstance(other, Value):
            other = Value(other)
        return Value(self.value - other.value)

    def __lt__(self, other):
        if not isinstance(other, Value):
            other = Value(other)
        return self.value < other.value

    def __gt__(self, other):
        if not isinstance(other, Value):
            other = Value(other)
        return self.value > other.value

    def __int__(self):
        return int(self.value)

    def __str__(self):
        return str(self.value)


class Measurements (deque):
    """extends deque by an average function"""
    def __init__(self, n=50):
        super(Measurements, self).__init__([], n)

    def avg(self):
        """provide average of items stored in the deque"""
        s = 0
        for v in self: 
            s += v.value
        return s // len(self)


class Lightness (threading.Thread):
    """threaded control of lightness"""
    def __init__(self, pin, lock):
        threading.Thread.__init__(self)
        self.__pin  = pin
        self.__lock = lock

        # SPI (MCP3008)
        self.__adc = MCP3008(SPI_const.CS0, 0, self.__lock)

        # Hardware PWM
        wipi.wiringPiSetupPhys()
        wipi.pinMode(self.__pin, 2)

        self.__running = True


    def run(self):
        target = Value(1023)
        measurements = Measurements()

        while (self.__running):
            actual = Value(self.__adc.read()+100)
            measurements.append(actual)
         
            avg = measurements.avg()
            if (avg > target+10):
                target += 2
            elif (avg < target-10):
                target -= 2
            elif (avg > target):
                target += 1
            elif (avg < target):
                target -= 1

            # target = 1000
            wipi.pwmWrite(self.__pin, int(1024-int(target)))  # TODO: Remove int(...
            # print("{}: Lightness (actual/avg/target): {}/{}/{}".format(time.strftime("%Y%m%d-%H%M%S"),actual,avg,target))
            time.sleep(0.1)

        self.__adc.close()

    def stop(self):
        """stops thread"""
        self.__running = False

### eof ###

