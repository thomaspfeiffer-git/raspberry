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


HEATING_PIN     = 38
HEATING_LATENCY = 60 * 15


# Misc for rrdtool
RRDFILE    = "/schild/weather/turtle.rrd"
DS_TEMP1   = "turtle_temp1"
DS_TEMP2   = "turtle_temp2"
DS_TEMP3   = "turtle_temp3"
DS_TEMPCPU = "turtle_tempcpu"
DS_HUMI    = "turtle_humi"
DS_HEATING = "turtle_heating"


# t0        = DS1820("/sys/bus/w1/devices/28-000006b4eb31/w1_slave")
# t1        = DS1820("/sys/bus/w1/devices/28-000006b58b12/w1_slave")
th        = DHT22_AM2302(21)   # BCM 21 = PIN 40
tc        = CPU()
heatlamp  = Heating(HEATING_PIN, HEATING_LATENCY)


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
   sys.exit()

def _Exit(s,f):
   Exit()


###############################################################################
# Main ########################################################################
def Main():
   schedule = [[5 for m in range(60)] for h in range(24)]
   schedule[ 7][0:59] = [25 for m in range(60)]
   schedule[ 8][0:59] = [25 for m in range(60)]
   schedule[ 9][0:59] = [25 for m in range(60)]
   schedule[10][0:59] = [20 for m in range(60)]
   schedule[11][0:59] = [20 for m in range(60)]
   schedule[12][0:59] = [25 for m in range(60)]
   schedule[13][0:59] = [25 for m in range(60)]
   schedule[14][0:59] = [20 for m in range(60)]
   schedule[15][0:59] = [18 for m in range(60)]
   schedule[16][0:29] = [17 for m in range(30)]

   m = [Measurements() for i in range(3)]

   while (True):
#      heatlamp.on()
      hh, mm  = localtime()[3:5]
      # t[0].append(t0.read())
      # t[1].append(t0.read())
      m[0].append(-99.9)
      m[1].append(-99.9)
      _t2, _h = th.read()
      m[2].append(_t2)
      _tc     = tc.read()

      if (schedule[hh][mm] > m[2].avg()):
         heatlamp.on()
      else:
         heatlamp.off()

      rrd_template = DS_TEMP1   + ":" + \
                     DS_TEMP2   + ":" + \
                     DS_TEMP3   + ":" + \
                     DS_TEMPCPU + ":" + \
                     DS_HUMI    + ":" + \
                     DS_HEATING
      rrd_data     = "N:{:.2f}".format(m[0].last()) + \
                      ":{:.2f}".format(m[1].last()) + \
                      ":{:.2f}".format(m[2].last()) + \
                      ":{:.2f}".format(_tc) + \
                      ":{:.2f}".format(_h) + \
                      ":{:}".format(heatlamp.status())
      print strftime("%H:%M:%S", localtime()), rrd_data
      rrdtool.update(RRDFILE, "--template", rrd_template, rrd_data) 

#      heatlamp.off()
      sleep(45)


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

finally:        # All cleanup is done in KeyboardInterrupt or signal handler. #
   pass

### eof ###

