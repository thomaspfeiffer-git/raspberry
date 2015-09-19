#############################################################################
# Reedcontact.py                                                            #
# (c) https://github.com/thomaspfeiffer-git 2015                            #
#############################################################################
""""""

import RPi.GPIO as io

class Reedcontact (object):
    def __init__(self, pin):
        self.__pin = pin
        self.__status = False

        def ___callback(pin):
            self.__status = io.input(pin)

        io.setmode(io.BOARD)
        io.setup(self.__pin,io.IN)
        io.add_event_detect(self.__pin,io.BOTH)
        io.add_event_callback(self.__pin,___callback)
        io.setup(self.__pin, io.IN, pull_up_down=io.PUD_UP)  


    def cleanup(self):
        io.remove_event_detect(self.__pin)


    def status (self):
        return 1 if self.__status else 0

### eof ###

