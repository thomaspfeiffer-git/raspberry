#!/usr/bin/python3 -u

import sys
import time

sys.path.append('../libs')
sys.path.append('../libs/sensors')

from Logging import Log
from DS1820 import DS1820

ds1820_1 = DS1820("/sys/bus/w1/devices/28-000006de80e2/w1_slave")
# ds1820_2 = DS1820("/sys/bus/w1/devices/28-000008386a83/w1_slave")

while True:
    Log("1: {}".format(ds1820_1.read_temperature()))
    # Log("2: {}".format(ds1820_2.read_temperature()))
    time.sleep(1)


