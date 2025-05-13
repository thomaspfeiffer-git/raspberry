#!/usr/bin/python3 -u

import sys
import time

sys.path.append('../libs')
sys.path.append('../libs/sensors')

from Logging import Log
from DS1820 import DS1820

ID = "28-030297946b71"

ds1820 = DS1820(f"/sys/bus/w1/devices/{ID}/w1_slave")

while True:
    Log(f"{ds1820.read_temperature()} °C")
    time.sleep(1)

# eof #

