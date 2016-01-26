#!/usr/bin/python
# -*- coding: utf-8 -*-


import RPi.GPIO as io
from time import sleep


pin_red    = 1
pin_orange = 2
pin_green  = 3


io.setmode(io.BOARD)
io.setup(pin_red, io.OUT)
io.setup(pin_orange, io.OUT)
io.setup(pin_green, io.OUT)


def GoRed ():
    io.output(pin_green, 1)
    sleep(1)
    io.output(pin_green, 0)
    sleep(1)
    io.output(pin_green, 1)
    sleep(1)
    io.output(pin_green, 0)
    sleep(1)
    io.output(pin_green, 1)
    sleep(1)
    io.output(pin_green, 0)
    sleep(1)
    io.output(pin_green, 1)
    sleep(1)
    io.output(pin_green, 0)
    io.output(pin_orange, 1)
    sleep(1)
    io.output(pin_orange, 0)
    io.output(pin_red, 1)



def GoGreen ():
    io.output(pin_orange, 1)
    sleep(1)
    io.output(pin_orange, 0)
    io.output(pin_red, 0)
    io.output(pin_green, 1)
     

while True:
    GoRed()
    sleep(10)
    GoGreen()
    sleep(10)

