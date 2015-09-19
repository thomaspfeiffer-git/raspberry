#############################################################################
# Reedcontact.py                                                            #
# (c) https://github.com/thomaspfeiffer-git 2015                            #
#############################################################################
""""""

import RPi.GPIO as io

class Reedcontact (object):


    def __init__(self, pin):
        self.__pin = pin
        self.__status = 0

        def ___callback(pin):
            self.__status = io.input(pin)

        io.setmode(io.BOARD)
        io.setup(self.__pin,io.IN)
        io.add_event_detect(self.__pin,io.BOTH)
        io.add_event_callback(self.__pin,___callback)
        io.setup(self.__pin, io.IN, pull_up_down=io.PUD_UP)  


    def __del__(self):
        print "in Reedcontact.__del__()"
        io.remove_event_detect(self.__pin)


    def status (self):
        return self.__status


### eof ###

