#!/usr/bin/python
# coding=utf-8


import RPi.GPIO as io
import time

from DS1820 import DS1820
from DHT22_AM2302 import DHT22_AM2302
from CPU import CPU



# Scheduler: https://docs.python.org/2/library/sched.html

# myArray=[[0 for j in range(3)] for i in range(3)]
schedule = [[5 for j in range(60)] for i in range(24)]


schedule[7][0]  = 5
schedule[7][1]  = 5
schedule[7][2]  = 5
schedule[7][3]  = 5
schedule[7][4]  = 5
schedule[7][5]  = 5
schedule[7][6]  = 5
schedule[7][7]  = 5
schedule[7][8]  = 5
schedule[7][9]  = 5

schedule[7][10] = 25
schedule[7][11] = 25
schedule[7][12] = 25
schedule[7][13] = 25
schedule[7][14] = 25
schedule[7][15] = 25
schedule[7][16] = 25
schedule[7][17] = 25
schedule[7][18] = 25
schedule[7][19] = 25

schedule[7][20] = 25
schedule[7][21] = 25
schedule[7][22] = 25
schedule[7][23] = 25
schedule[7][24] = 25
schedule[7][25] = 25
schedule[7][26] = 25
schedule[7][27] = 25
schedule[7][28] = 25
schedule[7][29] = 25


print schedule[7]


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


