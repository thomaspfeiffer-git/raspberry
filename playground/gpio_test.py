#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
##############################################################################
# gpio_test.py                                                               #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2019                  #
##############################################################################


#####


import sys
import time

sys.path.append('../libs')

from gpio import gpio as io
from Logging import Log
from Shutdown import Shutdown



###############################################################################
# Shutdown stuff ##############################################################
def shutdown_application ():
    """cleanup stuff"""
    Log("Stopping application")
    inp.close()
    led1.close()
    led2.close()
    Log("Application stopped")
    sys.exit(0)


###############################################################################
## main #######################################################################
if __name__ == "__main__":
    shutdown_application = Shutdown(shutdown_func=shutdown_application)

    led1 = io(65, io.OUT)
    led2 = io(66, io.OUT)
    inp  = io(67, io.IN)

    x = inp.read()
    print("x: {}".format(x))

    while True:
        led1.write("1")
        led2.write("0")
        time.sleep(0.5)
        led1.write("0")
        led2.write("1")
        time.sleep(0.5)

# eof #

