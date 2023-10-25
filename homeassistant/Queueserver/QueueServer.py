#!/usr/bin/python3
# -*- coding: utf-8 -*-
###############################################################################
# QueueServer.py                                                              #
# (c) https://github.com/thomaspfeiffer-git 2016, 2017                        #
###############################################################################
"""Server for messages of sensor values based on SensorQueueServer"""

import sys

sys.path.append('../../libs')
sys.path.append("../Queueserver/")
from SensorQueue import SensorQueueServer
from Shutdown import Shutdown


def shutdown_application ():
    """called on shutdown; stops all threads"""
    sys.exit(0)


if __name__ == '__main__':
    shutdown = Shutdown(shutdown_func=shutdown_application)
    SensorServer = SensorQueueServer("../config.ini")
    SensorServer.start()

### eof ###

