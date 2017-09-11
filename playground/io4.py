#!/usr/bin/python
# coding=utf-8
#############################################################################
# io4.py                                                                    #
# tests events on GPIO (seems to not work on NanoPi NEO Air)                #
# (c) https://github.com/thomaspfeiffer-git 2017                            #
#############################################################################



import RPi.GPIO as io
import time

pin = 7


io.setmode(io.BOARD)
io.setup(pin, io.IN) 


def my_callback (channel):
    print "callback on channel {}".format(channel)

io.add_event_detect(pin, io.RISING, callback=my_callback)      


try:
    while True:
        time.sleep(0.1)

finally:
    print "cleanup"
    io.cleanup()

# eof #

