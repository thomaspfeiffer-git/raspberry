#!/usr/bin/python
# -*- coding: utf-8 -*-
############################################################################
# Relais.py                                                                #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2017                #
############################################################################
"""control lighting of our anteroom:
   check relais and send status zu Anteroom main programm"""

### usage ###
# TODO
# sudo Relais.py

### setup ###
# TODO


import RPi.GPIO as io
import time

###############################################################################
## main ######################################################################

pin_ir = 7


io.setmode(io.BOARD)
io.setup(pin_ir, io.IN) 


last = None
while True:
    act = io.input(pin_ir)
    if act != last:
        if act == 1:
            # call url status == on
            pass
        else:
            # call url status == off
            pass

        last = act
        print("Status: {}".format(act))

    time.sleep(0.05)

# eof #

