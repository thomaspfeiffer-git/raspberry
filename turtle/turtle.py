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

   t_actual = [Measurements() for i in range(3)]

   while (True):
#      heatlamp.on()
      hh, mm  = localtime()[3:5]
      # _t0     = t0.read()
      # _t1     = t1.read()
      _t0     = -99.9
      _t1     = -99.9
      _t2, _h = th.read()
      _tc     = tc.read()

      t_actual[0].append(_t0)
      t_actual[1].append(_t1)
      t_actual[2].append(_t2)

      if (schedule[hh][mm] > t_actual[2].avg()):
         heatlamp.on()
      else:
         heatlamp.off()
      _s = heatlamp.status()

      rrd_template = DS_TEMP1   + ":" + \
                     DS_TEMP2   + ":" + \
                     DS_TEMP3   + ":" + \
                     DS_TEMPCPU + ":" + \
                     DS_HUMI    + ":" + \
                     DS_HEATING
      rrd_data     = "N:{:.2f}".format(_t0) + \
                      ":{:.2f}".format(_t1) + \
                      ":{:.2f}".format(_t2) + \
                      ":{:.2f}".format(_tc) + \
                      ":{:.2f}".format(_h) + \
                      ":{:}".format(_s)
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

