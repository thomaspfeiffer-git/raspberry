###############################################################################################
# Lightness.py                                                                                #
# Threaded class for control of lightness of LEDs                                             #
# (c) https://github.com/thomaspfeiffer-git May 2015                                          #
###############################################################################################

from collections import deque
import time
import threading
import wiringpi2 as wipi

from SPI_const import SPI_const
from MCP3008   import MCP3008


class Value (object):
   def __init__(self, v):
      self.value = v

   @property
   def value(self):
      return self.__value

   @value.setter
   def value(self,v):
      v = int(v)
      if (v >= 1023):
         self.__value = 1023
      elif (v <= 0):
         self.__value = 0
      else:
         self.__value = v

   def __add__(self, other):
      if not isinstance(other, Value):
         other = Value(other)
      return Value(self.value + other.value)

   def __sub__(self, other):
      if not isinstance(other, Value):
         other = Value(other)
      return Value(self.value - other.value)

   def __rsub__(self,other):
      return Value(other-self.value)

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


class Measurements (object):
   def __init__(self):
      self.__m = deque([],250)

   def add(self,v):
      self.__m.append(v)   # TODO: some check for type safety could be useful

   def avg(self):
      i = sum = 0
      for v in self.__m:
         sum += v.value
         i += 1
      return sum // i


class Lightness (threading.Thread):
   def __init__(self):
      threading.Thread.__init__(self)

      # SPI (MCP3008)
      self.__adc = MCP3008(SPI_const.CS0,0)

      # Hardware PWM
      wipi.wiringPiSetupPhys()
      wipi.pinMode(12,2)

      self.__running = True


   def run(self):
      target = Value(1023)
      measurements = Measurements()

      while (self.__running):
         actual = Value(self.__adc.read())
         measurements.add(actual)
         
         # Target is quite constant in intervall [avg-10, avg+10]. Thus lights do not jitter
         # on small changes of lightness.
         avg = measurements.avg()
         if (avg > target+10):
            target += 10
         elif (avg < target-10):
            target -= 10
         elif (avg > target):
            target += 1
         elif (avg < target):
            target -= 1

         wipi.pwmWrite(12,int(1024-target))
         # print("{}: Lightness (actual/avg/target): {}/{}/{}".format(time.strftime("%Y%m%d-%H%M%S"),actual,avg,target))
         time.sleep(0.1)


   def stop(self):
      self.__running = False

### eof ###

