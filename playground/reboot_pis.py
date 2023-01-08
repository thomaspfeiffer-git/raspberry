#!/usr/bin/python3
# -*- coding: utf-8 -*-
###############################################################################
# reboot_pis.py                                                               #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2023                   #
###############################################################################
"""
Hard reset:
Switches off power of some NanoPi Neo Air using relais.
"""

import argparse
import sys
import time

sys.path.append("../libs/")
from Logging import Log
from gpio import gpio as io


pin_nano02 = 66
pin_nano04 = 67
nano02 = 'nano02'
nano04 = 'nano04'

pins = { nano02: pin_nano02, nano04: pin_nano04 }


###############################################################################
## Switch #####################################################################
class Switch (object):
    def __init__ (self, pin):
        self.__io = io(pin, io.OUT, unexport=True)

    def on (self):
        self.__io.write("0")

    def off (self):
        self.__io.write("1")


###############################################################################
## Toggle #####################################################################
def Toggle (pi):
    s = Switch(pins[pi])
    s.off()
    time.sleep(10)
    s.on()


###############################################################################
## main #######################################################################
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('pi', choices=[nano02, nano04])
    args = parser.parse_args()
    Toggle(args.pi)

# eof #

