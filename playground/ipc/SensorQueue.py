#####################
#####################
"""bla"""


import threading

from multiprocessing.managers import BaseManager
import Queue



class SensorQueueConfig (object):
    PORT     = 50000
    HOSTNAME = "pia"
    AUTHKEY  = "finster war's, der mond schien helle"


class QueueManager(BaseManager): pass

class SensorQueueServer (threading.Thread):
    def __init__ (self):
        threading.Thread.__init__(self)    # TODO: use super(... ?

        self.__queue = Queue.Queue()
        QueueManager.register('get_queue', callable=lambda:self.__queue)
        m = QueueManager(address=('', SensorQueueConfig.PORT), authkey=SensorQueueConfig.AUTHKEY)
        self.__server = m.get_server()

        self.__running = True

    def run (self):
        self.__server.serve_forever()

    def stop(self):
        """stops thread"""
        self.__running = False


class SensorQueueClient (object):
    def __init__ (self):
        pass




# eof #

