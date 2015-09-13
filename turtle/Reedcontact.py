#############################################################################
# Reedcontact.py                                                            #
# (c) https://github.com/thomaspfeiffer-git 2015                            #
#############################################################################
""""""

import RPi.GPIO as io

class Reedcontact (object):
    def __callback(pin):
        print "callback:", pin

    def __init__(self, pin):
        self.__pin = pin
        self.__status = 0

        io.setmode(io.BOARD)
        io.setup(self.__pin,io.IN)

        # GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
        # GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  

        io.add_event_detect(self.__pin,io.BOTH)
        io.add_event_callback(seld.__pin,self.__callback)


        

    status (self):
        return self.__status


### eof ###

