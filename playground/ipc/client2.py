#!/usr/bin/python3

from SensorQueue import SensorQueueClient_read

sq = SensorQueueClient_read()

sv = sq.read()
print(sv)

