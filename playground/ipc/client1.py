#!/usr/bin/python

from multiprocessing.managers import BaseManager
import pickle

from sensorvalue import SensorValue

sv = SensorValue("TempWohnzimmer","temp")
sv.setValue(22.17)

class QueueManager(BaseManager): pass

QueueManager.register('get_queue')
m = QueueManager(address=('pia', 50000), authkey='abracadabra')
m.connect()
queue = m.get_queue()
queue.put(pickle.dumps(sv))
