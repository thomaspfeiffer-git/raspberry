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
sys.path.append('../libs/sensors')

from Logging import Log
from SDS011 import SDS011

sds011_1 = SDS011("/dev/ttyUSB0", use_query_mode=True)
#sds011_2 = SDS011("/dev/ttyUSB1", use_query_mode=True)


while True:
    sds011_1.sleep(sleep=False)
    #time.sleep(1)
    #sds011_2.sleep(sleep=False)
    time.sleep(15)

    for _ in range(3):
        v1 = sds011_1.query();
        #v2 = sds011_2.query();
        #if v1 is not None and v2 is not None:
        if v1 is not None:
            # Log("PM2.5: {}; PM10: {}".format(values[0],values[1]))
            #print("{},{},{},{}".format(v1[0],v1[1],v2[0],v2[1]))
            Log(",{0[0]},{0[1]}".format(v1))
        else:
            Log("v1 or v2 was None")
        time.sleep(3)    

    sds011_1.sleep()  
    #sds011_2.sleep()  
    time.sleep(300)

# eof #

