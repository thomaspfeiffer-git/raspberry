#!/usr/bin/python3 -u

import sys
import time


sys.path.append('../libs')
sys.path.append('../libs/sensors')

from Logging import Log
from SDS011 import SDS011

sds011 = SDS011("/dev/ttyUSB0", use_query_mode=True)


while True:
    sds011.sleep(sleep=False)
    time.sleep(15)

    values = sds011.query();
    if values is not None:
        # Log("PM2.5: {}; PM10: {}".format(values[0],values[1]))
        print("{},{}".format(values[0],values[1]))

    sds011.sleep()  
    time.sleep(300)

# eof #

