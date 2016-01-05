#!/usr/bin/python

from SensorQueue import SensorQueueClient_read

sq = SensorQueueClient_read()

while (True):
    sv = sq.read()
    print sv

