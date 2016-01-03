##############################################################################
# SensorQueue.py                                                             #
# Various classes for working with a queue in a client server architecture.  #
# (c) https://github.com/thomaspfeiffer-git 2016                             #
##############################################################################
"""
SensorQueue.py
Provides classes for working with a shared queue.

SensorQueueServer: Starts a server for working with the queue.
SensorQueueClient: Provides a client for the queue with methods 
                   for read from and write to the queue.
"""

from multiprocessing.managers import BaseManager
import pickle
import Queue


class SensorQueueConfig (object):
    """some constants for client server communication"""
    PORT     = 50000
    HOSTNAME = "pia"
    AUTHKEY  = "finster war's, der mond schien helle"


class QueueManager(BaseManager): 
    pass

class SensorQueueServer (object):
    """server class"""
    def __init__ (self):
        self.__queue = Queue.Queue()
        QueueManager.register('get_queue', callable=lambda:self.__queue)
        manager = QueueManager(address=('', SensorQueueConfig.PORT), \
                         authkey=SensorQueueConfig.AUTHKEY)
        self.__server = manager.get_server()

    def start (self):
        """starts the server"""
        print "server starting"
        try:
            self.__server.serve_forever()
        except KeyboardInterrupt:
            print "server stopped by ctrl-c"
        except SystemExit:
            print "server stopped by sigkill"

        print "server stopped (other reason)"


class SensorQueueClient (object):
    """client class providing methodes for read from and write to the queue"""
    def __init__ (self):
        QueueManager.register('get_queue')
        manager = QueueManager(address=(SensorQueueConfig.HOSTNAME, \
                                        SensorQueueConfig.PORT), \
                               authkey=SensorQueueConfig.AUTHKEY)
        manager.connect()
        self.__queue = manager.get_queue()

    def read (self):
        """read from the queue"""
        return pickle.loads(self.__queue.get())

    def write (self, item):
        """write to the queue"""
        self.__queue.put(pickle.dumps(item))

# eof #

