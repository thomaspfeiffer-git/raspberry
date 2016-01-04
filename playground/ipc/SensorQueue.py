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
import sys
from time import strftime, localtime, sleep


def Log (logstr):
    print strftime("%Y%m%d %H:%M:%S", localtime()), logstr


class SensorQueueConfig (object):
    """some constants for client server communication"""
    PORT       = 50000
    HOSTNAME   = "pia"
    AUTHKEY    = "finster war's, der mond schien helle"
    RETRYDELAY = 60


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
        self.__connected = False
        QueueManager.register('get_queue')
        self.__manager = QueueManager(address=(SensorQueueConfig.HOSTNAME, \
                                               SensorQueueConfig.PORT), \
                                      authkey=SensorQueueConfig.AUTHKEY)
        self.__connect()

    def __connect (self):
        """connects to the manager/server"""
        self.__connected = False
        while (not self.__connected):
            try:
                self.__manager.connect()
                self.__queue = self.__manager.get_queue()
                self.__connected = True
                Log("Connected to manager")
            except:
                Log("Cannot connect to manager: %s %s" % (sys.exc_info()[0], sys.exc_info()[1]))
                sleep(SensorQueueConfig.RETRYDELAY)


    def read (self):
        """read from the queue"""
        if (self.__connected):
            try:
                return pickle.loads(self.__queue.get())
            except Queue.Empty:
                Log("Queue empty")
            except:
                Log("Cannot read from queue: %s %s" % (sys.exc_info()[0], sys.exc_info()[1]))
                self.__connect()
        else:
            return "not connected" # TODO: raise exception or do other usefull stuff

    def write (self, item):
        """write to the queue"""
        if (self.__connected):
            try:
                self.__queue.put_nowait(pickle.dumps(item))
            except Queue.Full:
                Log("Queue full")
            except:
                Log("Cannot write to queue: %s %s" % (sys.exc_info()[0], sys.exc_info()[1]))
                self.__connect()

# eof #

