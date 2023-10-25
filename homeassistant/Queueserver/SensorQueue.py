##############################################################################
# SensorQueue.py                                                             #
# Various classes for working with a queue in a client server architecture.  #
# (c) https://github.com/thomaspfeiffer-git 2016, 2017                       #
##############################################################################
"""
SensorQueue.py
Provides classes for working with a shared queue.

SensorQueueServer: Starts a server for working with the queue.
SensorQueueClient: Provides a client for the queue with methods
                   for read from and write to the queue.
"""

import configparser
from datetime import datetime
from multiprocessing.managers import BaseManager
import pickle
import queue
from socket import gethostname
import sys
import time


def Log (logstr):
    """improved log output"""
    print("{}: {}".format(datetime.now().strftime("%Y%m%d %H:%M:%S"), logstr))


##############################################################################
class Error (Exception):
    """Base class for exceptions in this module."""
    pass

class HostnameError (Error):
    """Exception raised if the server script is not running on the
       configured server"""
    def __init__ (self, message):
        self.message = message

class NotConnectedError (Error):
    """Exception raised when a call to read() or write() is done
       to an unconnected queue"""
    def __init__ (self, message):
        self.message = message


##############################################################################
class SensorQueueConfig (object):
    """some constants for client server communication"""
    def __init__ (self, configfilename):
        config = configparser.ConfigParser()
        config.read(configfilename)

        self.HOSTNAME   = config['Queue']['Hostname']
        self.PORT       = int(config['Queue']['Port'])
        self.AUTHKEY    = config['Queue']['Key'].encode('latin1')
        self.RETRYDELAY = 60
        self.SERIALIZER = "pickle"


##############################################################################
class QueueManager(BaseManager):
    pass


##############################################################################
class SensorQueueServer (object):
    """server class"""
    def __init__ (self, configfilename):
        self.cfg = SensorQueueConfig(configfilename)

        if self.cfg.HOSTNAME != gethostname():
            raise HostnameError("configured hostname mismatches current server")

        self.__queue = queue.Queue()
        QueueManager.register('get_queue', callable=lambda:self.__queue)
        manager = QueueManager(address=('', self.cfg.PORT), \
                               authkey=self.cfg.AUTHKEY,    \
                               serializer=self.cfg.SERIALIZER)
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
        else:
            Log("server stopped (other reason)")


##############################################################################
class SensorQueueClient (object):
    """client class providing methodes for read from and write to the queue"""
    def __init__ (self, configfilename):
        self.cfg = SensorQueueConfig(configfilename)

        self.connected = False
        self.queue     = None

        QueueManager.register('get_queue')
        self.__manager = QueueManager(address=(self.cfg.HOSTNAME, \
                                               self.cfg.PORT),    \
                                      authkey=self.cfg.AUTHKEY,   \
                                      serializer=self.cfg.SERIALIZER)
        self.connect()

    def connect (self):
        """connects to the manager/server"""
        self.connected = False

        while not self.connected:
            try:
                self.__manager.connect()
                self.queue = self.__manager.get_queue()
                self.connected = True
                Log("Connected to manager")
            except:
                Log("Cannot connect to manager: {0}: {1[0]} {1[1]}".
                    format(self.__class__.__name__, sys.exc_info()))

                ### TODO: In case of outage of receiver, this ends up
                ### in an endless loop.
                for _ in range(self.cfg.RETRYDELAY):
                    time.sleep(1.0)



##############################################################################
class SensorQueueClient_write (SensorQueueClient):
    """write to queue as a thread"""
    def __init__ (self, configfilename):
        SensorQueueClient.__init__(self, configfilename)
        # TODO check super().__init ...
        self.__svl     = []

    def register (self, sensorvalue):
        """add another sensor and set function that is called by the
           sensorvalue when the value is updated"""
        self.__svl.append(sensorvalue)
        sensorvalue.setqueuefunc(self.write)

    def unregister (self, sensorvalue):
        """remove sensor from list"""
        self.__svl.remove(sensorvalue) # TODO: try/exception

    def write (self, item):
        """write to the queue"""
        if self.connected:
            try:
                try:
                    pickled = pickle.dumps(item)
                except:
                    Log("Cannot pickle: {0[0]} {0[1]}".format(sys.exc_info()))
                else:
                    self.queue.put_nowait(pickled)
            except KeyboardInterrupt:
                Log("ctrl-c")
                raise
            except queue.Full:
                Log("Queue full")
            except:
                Log("Cannot write to queue: {0[0]} {0[1]}".format(sys.exc_info()))
                ### TODO: In case of outage of receiver, this ends up
                ### in an endless loop.
                self.connect()
        else:
            raise NotConnectedError("write() called without connection to queue")


##############################################################################
class SensorQueueClient_read (SensorQueueClient):
    """read from queue"""
    def __init__ (self, configfilename):
        SensorQueueClient.__init__(self, configfilename)

    def read (self):
        """read from the queue"""
        if self.connected:
            try:
                return pickle.loads(self.queue.get_nowait())
            except queue.Empty:
                return None
            except SystemExit:
                raise
            except:
                Log("Cannot read from queue: {0[0]} {0[1]}".format(sys.exc_info()))
                self.connect()
        else:
            raise NotConnectedError("read() called without connection to queue")

# eof #

