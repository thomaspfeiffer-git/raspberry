#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# weather_feed.py                                                             #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2018                   #
###############################################################################
"""
Receives UDP data from our summer cottage and distributes it to the local
rrd database and to the sensor value queue.
"""

### usage ####
# TODO


import socket
import sys
import threading
import time

sys.path.append('../libs')

from Commons import Digest
from Logging import Log
from Shutdown import Shutdown


###############################################################################
###############################################################################
class UDP_Receiver (threading.Thread):
    def __init__ (self):
        threading.Thread.__init__(self)
        self._running = True

    def run (self):
        while self._running:
            Log("in UDP_Receiver.run()")
            time.sleep(10) # TODO: interruptible sleep

    def stop (self):
        self._running = False


###############################################################################
###############################################################################
class ToQueue (threading.Thread):
    def __init__ (self):
        threading.Thread.__init__(self)
        self._running = True

    def run (self):
        while self._running:
            Log("in ToQueue.run()")
            time.sleep(10) # TODO: interruptible sleep

    def stop (self):
        self._running = False


###############################################################################
###############################################################################
class ToRRD (threading.Thread):
    def __init__ (self):
        threading.Thread.__init__(self)
        self._running = True

    def run (self):
        while self._running:
            Log("in ToRRD.run()")
            time.sleep(10) # TODO: interruptible sleep

    def stop (self):
        self._running = False


###############################################################################
# shutdown ####################################################################
def shutdown_application ():
    """cleanup stuff"""
    Log("Stopping application")
    to_rrd.stop()
    to_rrd.join()
    to_queue.stop()
    to_queue.join()
    udp.stop()
    udp.join()
    Log("Application stopped")
    sys.exit(0)


###############################################################################
# main ########################################################################
if __name__ == '__main__':
    shutdown_application = Shutdown(shutdown_func=shutdown_application)

    udp = UDP_Receiver()
    to_queue = ToQueue()
    to_rrd = ToRRD()

    udp.start()
    to_queue.start()
    to_rrd.start()

    while True:
        time.sleep(120)

# eof #

