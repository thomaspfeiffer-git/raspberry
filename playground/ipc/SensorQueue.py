#####################
#####################
"""bla"""

from multiprocessing.managers import BaseManager
import pickle
import Queue


class SensorQueueConfig (object):
    PORT     = 50000
    HOSTNAME = "pia"
    AUTHKEY  = "finster war's, der mond schien helle"


class QueueManager(BaseManager): pass

class SensorQueueServer (object):
    def __init__ (self):
        self.__queue = Queue.Queue()
        QueueManager.register('get_queue', callable=lambda:self.__queue)
        m = QueueManager(address=('', SensorQueueConfig.PORT), authkey=SensorQueueConfig.AUTHKEY)
        self.__server = m.get_server()

    def start (self):
        print "server starting"
        self.__server.serve_forever()


class SensorQueueClient (object):
    def __init__ (self):
        QueueManager.register('get_queue')
        m = QueueManager(address=(SensorQueueConfig.HOSTNAME, SensorQueueConfig.PORT), authkey=SensorQueueConfig.AUTHKEY)
        m.connect()
        self.__queue = m.get_queue()

    def read (self):
        return pickle.loads(self.__queue.get())

    def write (self, item):
        self.__queue.put(pickle.dumps(item))

# eof #

