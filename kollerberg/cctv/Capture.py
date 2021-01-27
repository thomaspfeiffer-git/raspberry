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
# TakePictures ################################################################
class TakePictures(object):
    def __init__(self, queue):
        self.queue = queue

    def run(self):
        self._running = True

        i = 0
        while self._running:
            Log(f"Putting '{i}' to queue")
            self.queue.put(i)
            i += 1
            time.sleep(0.5)

    def stop(self):
        self._running = False


###############################################################################
# Deliver #####################################################################
class Deliver(object):
    def __init__(self, queue):
        self.queue = queue

    def run(self):
        self._running = True

        while self._running:
            item = self.queue.get()
            Log(f"Got '{item}' from queue")
            self.queue.task_done()
            time.sleep(1)

    def stop(self):
        self._running = False


###############################################################################
# Main ########################################################################
if __name__ == '__main__':
    queue = queue.Queue(maxsize=5)


# eof #
