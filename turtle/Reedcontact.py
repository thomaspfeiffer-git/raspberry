#############################################################################
# Reedcontact.py                                                            #
# (c) https://github.com/thomaspfeiffer-git 2015                            #
#############################################################################
""""""

import RPi.GPIO as io

class Reedcontact (object):
    __callback(pin):
        print "callback:", pin

    __init__(self, pin):
        self.__pin = pin

        io.setmode(io.BOARD)
        io.setup(self.__pin,io.IN)
        io.add_event_detect(self.__pin,io.BOTH)
        io.add_event_callback(seld.__pin,self.__callback)
        



### eof ###

