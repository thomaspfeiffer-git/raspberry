#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import wiringpi2 as wipi

PIN = 12 # BCM GPIO 18
wipi.wiringPiSetupPhys()
wipi.pinMode(PIN, 2)

i = 0
while True:
    wipi.pwmWrite(PIN, i % 1024)
    i += 1
    time.sleep(0.01)
    print(i)

