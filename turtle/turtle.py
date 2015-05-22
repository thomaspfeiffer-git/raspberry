#!/usr/bin/python
# coding=utf-8


import RPi.GPIO as io
import time

from DS1820 import DS1820
from DHT22_AM2302 import DHT22_AM2302
from CPU import CPU


t1 = DS1820("/sys/bus/w1/devices/28-000006b4eb31/w1_slave")
t2 = DS1820("/sys/bus/w1/devices/28-000006b58b12/w1_slave")
th = DHT22_AM2302(21)   # BCM 21 = PIN 40
tc = CPU()



################################################################################
# IO für Relais ################################################################

io.setmode(io.BOARD)
io.setup(38,io.OUT)
#io.output(38,io.HIGH)
#time.sleep(2)
#io.output(38,io.LOW)
io.cleanup()



print "T1:", t1.read()
print "T2:", t2.read()
t3, h = th.read()
print "T3:", t3
print "H:", h
print "CPU:", tc.read()


