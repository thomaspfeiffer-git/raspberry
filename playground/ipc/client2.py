#!/usr/bin/python

from SensorQueue import SensorQueueClient

sq = SensorQueueClient()

while (True):
    sv = sq.read()
    print sv

