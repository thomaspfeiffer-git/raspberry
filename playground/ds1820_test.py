#!/usr/bin/python3

import sys
import time

sys.path.append('../libs')
sys.path.append('../libs/sensors')

from Logging import Log
from DS1820 import DS1820

ds1820 = DS1820("/sys/bus/w1/devices/28-000008561957/w1_slave")

while True:
    Log(ds1820.read_temperature())
    time.sleep(10)


