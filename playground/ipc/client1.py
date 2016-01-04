#!/usr/bin/python

from time import sleep

from SensorQueue import SensorQueueClient
from SensorValue import SensorValue

sq = SensorQueueClient()
sv = SensorValue("TempWohnzimmer","temp")


i = 0
while (True):
    sv.value = i
    sq.write(sv)
    i += 1
    sleep(25)
