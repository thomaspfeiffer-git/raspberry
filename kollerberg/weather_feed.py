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

sys.path.append('../libs')

from Commons import Digest
from Logging import Log
from Shutdown import Shutdown


###############################################################################
###############################################################################
class UDP_Receiver (threading.Thread):
    pass



###############################################################################
###############################################################################
class ToQueue (threading.Thread):
    pass



###############################################################################
###############################################################################
class ToRRD (threading.Thread):
    pass



###############################################################################
# shutdown ####################################################################
def shutdown_application ():
    """cleanup stuff"""
    Log("Stopping application")
    Log("Application stopped")
    sys.exit(0)


###############################################################################
# main ########################################################################
if __name__ == '__main__':
    shutdown_application = Shutdown(shutdown_func=shutdown_application)



# eof #

