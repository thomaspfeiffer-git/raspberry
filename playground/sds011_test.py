#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
##############################################################################
# ds011_test.py                                                              #
# Testing air quality sensor SDS011                                          #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2018                  #
##############################################################################

import sys
import time

sys.path.append('../libs')

from Logging import Log
from Shutdown import Shutdown

from sensors.SDS011 import SDS011

sds011_1 = SDS011("/dev/ttyUSB0", use_query_mode=True)
# sds011_2 = SDS011("/dev/ttyUSB1", use_query_mode=True)


###############################################################################
# Shutdown stuff ##############################################################
def shutdown_application ():
    """cleanup stuff"""
    Log("Stopping application")
    sds011_1.close()
#    sds011_2.close()
    Log("Application stopped")
    sys.exit(0)


###############################################################################
## main #######################################################################
if __name__ == "__main__":
    shutdown_application = Shutdown(shutdown_func=shutdown_application)

    while True:
        sds011_1.sleep(sleep=False)
#        time.sleep(1)
#        sds011_2.sleep(sleep=False)
        time.sleep(25)

        for _ in range(3):
            v1 = sds011_1.query();
            Log(",{0[0]},{0[1]}".format(v1))
            time.sleep(3)    
            """
            v2 = sds011_2.query();
            if v1 is not None and v2 is not None:
                # Log("PM2.5: {}; PM10: {}".format(values[0],values[1]))
                #print("{},{},{},{}".format(v1[0],v1[1],v2[0],v2[1]))
                Log(",{0[0]},{0[1]},{1[0]},{1[1]}".format(v1,v2))
            else:
                Log("v1 or v2 was None")
            time.sleep(3)    
            """

        sds011_1.sleep()  
#        sds011_2.sleep()  
        time.sleep(60)

# eof #

