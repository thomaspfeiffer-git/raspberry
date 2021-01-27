#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# Capture.py                                                                  #
# (c) https://github.com/thomaspfeiffer-git 2021                              #
###############################################################################
"""
"""

### usage ###

import queue
import threading
import time
import sys

sys.path.append('../../libs')
from Shutdown import Shutdown
from Logging import Log


###############################################################################
# Daylight ####################################################################
class Daylight(object):
    def __init__(self):
        pass

    def run(self):
        self._running = True
        while self._running:
            time.sleep(0.1)

    def stop(self):
        self._running = False


###############################################################################
# TakePictures ################################################################
class TakePictures(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        self._running = True

        i = 0
        while self._running:
            Log(f"Putting '{i}' to queue")
            self.queue.put(i)
            i += 1
            time.sleep(0.1)
        Log("'TakePictures' stopped")

    def stop(self):
        Log("Stopping 'TakePictures'")
        self._running = False


###############################################################################
# Deliver #####################################################################
class Deliver(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        self._running = True

        while self._running:
            item = self.queue.get()
            Log(f"Got '{item}' from queue")
            self.queue.task_done()
            time.sleep(1)
        Log("'Deliver' stopped")

    def stop(self):
        Log("Stopping 'Deliver'")
        self._running = False


###############################################################################
# shutdown_application ########################################################
def shutdown_application():
    """called on shutdown; stops all threads"""
    Log("Stopping application.")
    deliver.stop()
    deliver.join()
    pictures.stop()
    pictures.join()
    Log("Application stopped.")
    sys.exit(0)


###############################################################################
# Main ########################################################################
if __name__ == '__main__':
    shutdown = Shutdown(shutdown_func=shutdown_application)
    queue = queue.Queue(maxsize=5)

    pictures = TakePictures(queue)
    pictures.start()

    deliver = Deliver(queue)
    deliver.start()

    while True:
        time.sleep(0.1)

# eof #
