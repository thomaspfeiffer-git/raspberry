#!/usr/bin/python
# -*- coding: utf-8 -*-


import RPi.GPIO as io
from time import sleep


pin_red    = 15
pin_orange = 36
pin_green  = 33


io.setmode(io.BOARD)
io.setup(pin_red, io.OUT)
io.setup(pin_orange, io.OUT)
io.setup(pin_green, io.OUT)

io.output(pin_green, 0)
io.output(pin_orange, 0)
io.output(pin_red, 0)


def GoRed ():
    io.output(pin_green, 1)
    sleep(0.5)
    io.output(pin_green, 0)
    sleep(0.5)
    io.output(pin_green, 1)
    sleep(0.5)
    io.output(pin_green, 0)
    sleep(0.5)
    io.output(pin_green, 1)
    sleep(0.5)
    io.output(pin_green, 0)
    sleep(0.5)
    io.output(pin_green, 1)
    sleep(0.5)
    io.output(pin_green, 0)
    io.output(pin_orange, 1)
    sleep(2)
    io.output(pin_orange, 0)
    io.output(pin_red, 1)



def GoGreen ():
    io.output(pin_orange, 1)
    sleep(2)
    io.output(pin_orange, 0)
    io.output(pin_red, 0)
    io.output(pin_green, 1)
     

while True:
    GoRed()
    sleep(10)
    GoGreen()
    sleep(10)

