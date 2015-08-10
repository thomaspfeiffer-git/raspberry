#!/usr/bin/python
# coding=utf-8

from collections import deque
import rrdtool
import signal
import sys
from time import *
import traceback


from CPU import CPU
from DHT22_AM2302 import DHT22_AM2302
from DS1820 import DS1820
from Heating import Heating
import Schedules


HEATLAMP_PIN      = 38
HEATLAMP_LATENCY  = 60 * 15

LIGHTLAMP_PIN     = 36
LIGHTLAMP_LATENCY = 60 * 15


# Misc for rrdtool
RRDFILE     = "/schild/weather/turtle.rrd"
DS_TEMP1    = "turtle_temp1"
DS_TEMP2    = "turtle_temp2"
DS_TEMP3    = "turtle_temp3"
DS_TEMPCPU  = "turtle_tempcpu"
DS_HUMI     = "turtle_humi"
DS_HEATING  = "turtle_heating"
DS_LIGHTING = "turtle_lighting"


t1        = DS1820("/sys/bus/w1/devices/28-000006d62eb1/w1_slave")
t2        = DS1820("/sys/bus/w1/devices/28-000006dd6ac1/w1_slave")
th        = DHT22_AM2302(21)   # BCM 21 = PIN 40
tc        = CPU()
heatlamp  = Heating(HEATLAMP_PIN, HEATLAMP_LATENCY)
lightlamp = Heating(LIGHTLAMP_PIN, LIGHTLAMP_LATENCY)



###############################################################################
# Measurements ################################################################
class Measurements (deque):
   def __init__(self, n=5):
      super(Measurements,self).__init__([],n)

   def avg(self):
      return sum(list(self)) / float(len(self))

   def last(self):
      return self[len(self)-1]


###############################################################################
# Exit ########################################################################
def Exit():
   heatlamp.cleanup()
   lightlamp.cleanup()
   sys.exit()

def _Exit(s,f):
   Exit()


###############################################################################
# Main ########################################################################
def Main():
   heatcontrol  = Schedules.Control(Schedules.ScheduleHeat(),heatlamp)
   lightcontrol = Schedules.Control(Schedules.ScheduleLight(),lightlamp)

   m = {DS_TEMP1:   Measurements(), \
        DS_TEMP2:   Measurements(), \
        DS_TEMP3:   Measurements(), \
        DS_TEMPCPU: Measurements(), \
        DS_HUMI:    Measurements()}
 
   while (True):
      m[DS_TEMP1].append(t1.read())
      m[DS_TEMP2].append(t2.read())
      _t3, _h = th.read()
      m[DS_TEMP3].append(_t3)
      m[DS_HUMI].append(_h)
      m[DS_TEMPCPU].append(tc.read())

      heatcontrol.control(m[DS_TEMP3].avg())
      lightcontrol.control(m[DS_TEMP3].avg())

      rrd_template = DS_TEMP1   + ":" + \
                     DS_TEMP2   + ":" + \
                     DS_TEMP3   + ":" + \
                     DS_TEMPCPU + ":" + \
                     DS_HUMI    + ":" + \
                     DS_HEATING + ":" + \
                     DS_LIGHTING
                     
      rrd_data     = "N:{:.2f}".format(m[DS_TEMP1].last()) + \
                      ":{:.2f}".format(m[DS_TEMP2].last()) + \
                      ":{:.2f}".format(m[DS_TEMP3].last()) + \
                      ":{:.2f}".format(m[DS_TEMPCPU].last()) + \
                      ":{:.2f}".format(m[DS_HUMI].last()) + \
                      ":{:}".format(heatlamp.status())    + \
                      ":{:}".format(lightlamp.status())
      print strftime("%H:%M:%S", localtime()), rrd_data
      rrdtool.update(RRDFILE, "--template", rrd_template, rrd_data) 

      sleep(35)


###############################################################################
###############################################################################
signal.signal(signal.SIGTERM, _Exit)

try:
   Main()

except KeyboardInterrupt:
   Exit()

except SystemExit:                  # Done in signal handler (method _Exit()) #
   pass

except:
   print(traceback.print_exc())
   Exit()

finally:        # All cleanup is done in KeyboardInterrupt or signal handler. #
   pass

### eof ###

