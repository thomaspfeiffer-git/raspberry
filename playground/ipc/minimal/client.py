#!/usr/bin/python3

from multiprocessing.managers import BaseManager

class QueueManager(BaseManager): 
    pass

manager = QueueManager(address=('', 50001), authkey="hallo".encode('latin1'))
manager.connect()

