#!/usr/bin/python

from multiprocessing.managers import BaseManager

try:
    import queue
except ImportError:
    import Queue as queue

class QueueManager(BaseManager): 
    pass

q = queue.Queue()
QueueManager.register('get_queue', callable=lambda:q)
manager = QueueManager(address=('', 50001), authkey="hallo".encode('latin1'), serializer="xmlrpclib")
server = manager.get_server()
server.serve_forever()

