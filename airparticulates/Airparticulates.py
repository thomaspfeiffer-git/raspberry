#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# Airparticulates.py                                                          #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2018                   #
###############################################################################

"""
"""

import sys
import time


sys.path.append("../libs/")
from Logging import Log
from Shutdown import Shutdown

from sensors.SDS011 import SDS011


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

    while True:
        pass



# eof #

