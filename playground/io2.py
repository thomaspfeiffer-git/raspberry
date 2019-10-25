#!/usr/bin/python3 -u
# coding=utf-8


import RPi.GPIO as io
import time

pin_ir = 7


io.setmode(io.BOARD)
io.setup(pin_ir, io.IN) 

last = None
while True:
    act = io.input(pin_ir)
    if act != last:
        last = act
        print("Status: {}".format(act))

    time.sleep(0.05)

# eof #

