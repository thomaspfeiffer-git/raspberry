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
import threading


def Log (logstr):
    """improved log output"""
    print strftime("%Y%m%d %H:%M:%S", localtime()), logstr


class SensorQueueConfig (object):
    """some constants for client server communication"""
    PORT       = 50000
    HOSTNAME   = "pia"
    AUTHKEY    = "finster war's, der mond schien helle"
    RETRYDELAY = 60
    SENDDELAY  = 60


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
        Log("server starting")
        try:
            self.__server.serve_forever()
        except KeyboardInterrupt:
            Log("server stopped by ctrl-c")
        except SystemExit:
            Log("server stopped by sigkill")

        Log("server stopped (other reason)")


class SensorQueueClient (threading.Thread):
    """client class providing methodes for read from and write to the queue"""
    # TODO: expand documentation for threading and sensorvalue lock
    # TODO: Consider separation of read and write process
    #       class SensorQueueClient_read
    #       class SensorQueueClient_write
    def __init__ (self):
        threading.Thread.__init__(self)
        self.__connected = False
        self.__queue     = None
        self.__svl       = []

        QueueManager.register('get_queue')
        self.__manager = QueueManager(address=(SensorQueueConfig.HOSTNAME, \
                                               SensorQueueConfig.PORT), \
                                      authkey=SensorQueueConfig.AUTHKEY)
        self.__connect()
        self.__running = True


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
                Log("Cannot connect to manager: %s %s" % \
                    (sys.exc_info()[0], sys.exc_info()[1]))
                sleep(SensorQueueConfig.RETRYDELAY)

    def register (self, sensorvaluelock):
         self.__svl.append(sensorvaluelock) 

    def unregister (self, sensorvaluelock):
         self.__svl.remove(sensorvaluelock) # TODO: try/exception

    def run (self):
        """start thread. loop: send data to queue and sleep"""
        while self.__running:
            for sensor in self.__svl:
                with sensor.lock:
                    item = sensor.sensorvalue  # copy data from sensor
                Log("in run: %s" % item)
                self.write(item)                   # write data to queue

            for _ in range(SensorQueueConfig.SENDDELAY):
                sleep (1)
                if not self.__running:
                    break

    def stop (self):
        """stops the running thread"""
        self.__running = False

    def read (self):
        """read from the queue"""
        if (self.__connected):
            try:
                return pickle.loads(self.__queue.get())
            except KeyboardInterrupt:
                Log("ctrl-c")
                raise
            except Queue.Empty:
                Log("Queue empty")
            except:
                Log("Cannot read from queue: %s %s" % \
                    (sys.exc_info()[0], sys.exc_info()[1]))
                self.__connect()
            return "had an exception" # TODO: improve message
        else:
            return "not connected" # TODO: raise exception or do other usefull stuff

    def write (self, item):
        """write to the queue"""
        if (self.__connected):
            try:
                self.__queue.put_nowait(pickle.dumps(item))
            except KeyboardInterrupt:
                Log("ctrl-c")
                raise
            except Queue.Full:
                Log("Queue full")
            except:
                Log("Cannot write to queue: %s %s" % \
                    (sys.exc_info()[0], sys.exc_info()[1]))
                self.__connect()

# eof #

