#!/usr/bin/python3

import sys

sys.path.append('../libs')
sys.path.append('../libs/sensors')

from DS1820 import DS1820

ds1820 = DS1820("/sys/bus/w1/devices/28-000006b50d05/w1_slave")

print(ds1820.read_temperature())


