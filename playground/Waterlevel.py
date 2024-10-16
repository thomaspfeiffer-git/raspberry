#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# TODO                                                                        #
# (c) https://github.com/thomaspfeiffer-git 2024                              #
###############################################################################

"""
"""

"""
###### Usage ######
# TODO
"""


import os
import sys
import time

sys.path.append("../libs/")
from Logging import Log
from Shutdown import Shutdown
import UDP


CREDENTIALS = os.path.expanduser("~/credentials/waterlevel.cred")


###############################################################################
# Receiver ####################################################################
class Receiver (object):
    def __init__ (self):
        self.udp = UDP.Receiver(CREDENTIALS)

    def run (self):
        while True:
            payload = self.udp.receive()


###############################################################################
# Shutdown stuff ##############################################################
def shutdown_application ():
    """cleanup stuff"""
    Log("Stopping application")
    Log("Application stopped")
    sys.exit(0)


###############################################################################
## main #######################################################################
if __name__ == "__main__":
    shutdown_application = Shutdown(shutdown_func=shutdown_application)

    r = Receiver()
    r.run()

# eof #

