#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# udp.py                                                                      #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2018                   #
###############################################################################
"""
Basic data transfer using UDP.
"""


import sys

sys.path.append("../libs/")
from Logging import Log
from Shutdown import Shutdown


###############################################################################
# Sender ######################################################################
class Sender (object):
    pass




###############################################################################
# Receiver ####################################################################
class Receiver (object):
    pass



###############################################################################
# shutdown ####################################################################
def shutdown_application ():
    """cleanup stuff"""
    Log("Stopping application")
    Log("Application stopped")
    sys.exit(0)


###############################################################################
## main #######################################################################
if __name__ == "__main__":
    shutdown_application = Shutdown(shutdown_func=shutdown_application)




# eof #

