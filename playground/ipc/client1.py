#!/usr/bin/python

from time import sleep

from SensorQueue import SensorQueueClient
from sensorvalue import SensorValue

sq = SensorQueueClient()
sv = SensorValue("TempWohnzimmer","temp")


i = 0
while (True):
    sv.setValue(i)
    sq.write(sv)
    i += 1
    sleep(55)
