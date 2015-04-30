#!/usr/bin/python

import wiringpi2 as wipi

wipi.wiringPiSetupPhys()

wipi.pinMode(12,2)
wipi.pwmWrite(12,900)

