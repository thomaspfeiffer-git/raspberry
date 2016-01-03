#!/usr/bin/python

from multiprocessing.managers import BaseManager
import pickle


class QueueManager(BaseManager): pass
QueueManager.register('get_queue')
m = QueueManager(address=('pia', 50000), authkey='abracadabra')
m.connect()
queue = m.get_queue()
sv = pickle.loads(queue.get())

sv.showContent()

