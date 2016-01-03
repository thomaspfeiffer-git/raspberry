#!/usr/bin/python

from multiprocessing.managers import BaseManager
import pickle
from time import sleep

from sensorvalue import SensorValue

sv = SensorValue("TempWohnzimmer","temp")

class QueueManager(BaseManager): pass

QueueManager.register('get_queue')
m = QueueManager(address=('pia', 50000), authkey='abracadabra')
m.connect()
queue = m.get_queue()

i = 0
while (True):
    sv.setValue(i)
    queue.put(pickle.dumps(sv))
    i += 1
    sleep(55)
