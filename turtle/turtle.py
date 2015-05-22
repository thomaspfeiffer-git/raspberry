#!/usr/bin/python
# coding=utf-8


import time

from CPU import CPU
from DHT22_AM2302 import DHT22_AM2302
from DS1820 import DS1820
from Heating import Heating



# Scheduler: https://docs.python.org/2/library/sched.html

schedule = [[5 for m in range(60)] for h in range(24)]
schedule[ 7][0:59] = [25 for m in range(60)]
schedule[ 8][0:59] = [25 for m in range(60)]
schedule[ 9][0:59] = [25 for m in range(60)]
schedule[10][0:59] = [20 for m in range(60)]
schedule[11][0:59] = [20 for m in range(60)]
schedule[12][0:59] = [25 for m in range(60)]
schedule[13][0:59] = [25 for m in range(60)]
schedule[14][0:59] = [20 for m in range(60)]
schedule[15][0:59] = [20 for m in range(60)]
schedule[16][0:59] = [20 for m in range(60)]
schedule[17][0:59] = [20 for m in range(60)]


t1 = DS1820("/sys/bus/w1/devices/28-000006b4eb31/w1_slave")
t2 = DS1820("/sys/bus/w1/devices/28-000006b58b12/w1_slave")
th = DHT22_AM2302(21)   # BCM 21 = PIN 40
tc = CPU()

heatlamp  = Heating(38)

# if (schedule[hh][mm] > t2):
#    Heizung_ein
# else:
#    Heizung aus
# if (schalter wurd aus oder eingeschaltet (also bei änderung): 
#    sleep 10 Min ==> Hystere


heatlamp.on()


print "T1:", t1.read()
print "T2:", t2.read()
t3, h = th.read()
print "T3:", t3
print "H:", h
print "CPU:", tc.read()

heatlamp.off()

heatlamp.cleanup()
