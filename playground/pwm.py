#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import wiringpi2 as wipi

PIN = 18
wipi.wiringPiSetupPhys()
wipi.pinMode(PIN, 2)

i = 0
while True:
    wipi.pwmWrite(PIN, i % 1024)
    i += 1
    time.sleep(0.1)




