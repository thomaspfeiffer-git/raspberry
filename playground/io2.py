#!/usr/bin/python3
# coding=utf-8


import RPi.GPIO as io
import time

pin_ir = 37


io.setmode(io.BOARD)
io.setup(pin_ir, io.IN) 

while True:
    print(io.input(pin_ir))
    time.sleep(0.5)


