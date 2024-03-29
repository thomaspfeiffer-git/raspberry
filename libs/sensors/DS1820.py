# -*- coding: utf-8 -*-
##############################################################################
# DS1820.py                                                                  #
# Communication with DS1820                                                  #
# (c) https://github.com/thomaspfeiffer-git May 2015, 2016, 2017, 2023       #
##############################################################################

import re
import time
import sys
import threading


class Consume_CPU (threading.Thread):
    """cause of some timing issues of the kernel implementation
       of the 1-wire bus, we need some cpu consuming tasks. For
       more details refer to
       http://www.friendlyarm.com/Forum/viewtopic.php?f=47&t=393 """

    def __init__ (self):
        threading.Thread.__init__(self)
        self.__running = True

    def run (self):
        i = 0
        while self.__running:
            j = i * i
            jj = i * i * i
            jjj = j * i
            if i > 10000000000:
                i = 0

    def stop (self):
        self.__running = False


class DS1820:
   def __init__ (self, id):
       self.__id          = id
       self.__lastvalue   = 0

   def __read_sensor (self):
       try:
           with open(self.__id, "r") as f:
               line = f.readline()
               if re.match(r"([0-9a-f]{2} ){9}: crc=[0-9a-f]{2} YES", line):
                   line = f.readline()
                   m = re.match(r"([0-9a-f]{2} ){9}t=([+-]?[0-9]+)", line)
                   if m:
                       self.__lastvalue = float(m.group(2)) / 1000.0

       except IOError as e:
           print(time.strftime("%Y%m%d %X"), "Error reading", self.__id, ": ", e)

       finally:
           return self.__lastvalue

   def consume_cpu_start (self):
       self.__consume_cpu = Consume_CPU()
       self.__consume_cpu.start()

           # after starting the cpu consuming task, it takes a couple of
           # seconds until the 1-wire device appears in /sys/bus/w1/devices/.
       time.sleep(10)


   def consume_cpu_stop (self):
       self.__consume_cpu.stop()
       self.__consume_cpu.join()


   def read_temperature (self):
       return self.__read_sensor()

### eof ###

