#!/usr/bin/python
# coding=utf-8
#############################################################################
# hibernation.py                                                            #
# Have a great hibernation for our turtle.                                  #
# (c) https://github.com/thomaspfeiffer-git 2015                            #
#############################################################################
"""Have a great hibernation for our turtle."""

import datetime
import rrdtool
import signal
import sys
from time import strftime, localtime, sleep, time
import traceback

from CPU import CPU
from DHT22_AM2302 import DHT22_AM2302
from DS1820 import DS1820
from Heating import Heating
from Measurements import Measurements
from Reedcontact import Reedcontact


DHT22_AM2302_PIN = 40

REEDCONTACT_PIN  = 38
REED_STRETCH     = 60 * 3

FRIDGE_PIN       = 36
FRIDGE_LATENCY   = 60


# File for monitoring
MONITORING  = "turtle_monitoring.log"


# Misc for rrdtool
RRDFILE    = "hibernation.rrd"
DS_TEMP1   = "hibernation_temp1"
DS_TEMPCPU = "hibernation_tempcpu"
DS_TEMP2   = "hibernation_temp2"
DS_HUMI    = "hibernation_humi"
DS_ON      = "hibernation_on"
DS_OPEN    = "hibernation_open"


fridge = Heating(FRIDGE_PIN, FRIDGE_LATENCY)
reedcontact = Reedcontact(REEDCONTACT_PIN, REED_STRETCH)
reedcontact.start()



def writeMonitoringData(rrd_data):
    """write various data to a file used for monitoring"""
    with open(MONITORING, 'w') as f:
        ts = time()
        f.write(datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S:") + str(ts) + ":" + rrd_data)



###############################################################################
# Main ########################################################################
def main():
    """main part"""
    temp_fridge = DS1820("/sys/bus/w1/devices/28-000006dc8d42/w1_slave")
    temp_cpu    = CPU()
    temphumi    = DHT22_AM2302(21)   # BCM 21 = PIN 40

    measurements = {DS_TEMP1:   Measurements(3), \
                    DS_TEMPCPU: Measurements(3), \
                    DS_TEMP2:   Measurements(3), \
                    DS_HUMI:    Measurements(3)}

    rrd_template = DS_TEMP1   + ":" + \
                   DS_TEMPCPU + ":" + \
                   DS_TEMP2   + ":" + \
                   DS_HUMI    + ":" + \
                   DS_ON      + ":" + \
                   DS_OPEN

    while (True):
        measurements[DS_TEMP1].append(temp_fridge.read())
        measurements[DS_TEMPCPU].append(temp_cpu.read())

        _temp, _humi = temphumi.read()
        measurements[DS_TEMP2].append(_temp)
        measurements[DS_HUMI].append(_humi)

#        if (measurements[DS_TEMP1].avg() > 5.8):
##        if (measurements[DS_TEMP1].avg() > -20.0):
#            fridge.on()
#        if (measurements[DS_TEMP1].avg() < 5.6):
#            fridge.off()
        fridge.off()



# if (temp > 6): fridge.on()
# else if (temp > 5): 
#   fridge_on_time(60,90) # für 60 sekunden einschalten; 90 Sekunden mindestens aus
# else if (temp < 5.0): 
#   fridge.off()


# class fridge_... derived from class Heating

# threading: https://docs.python.org/2/library/threading.html
# multi inheritance:  https://docs.python.org/2/tutorial/classes.html#multiple-inheritance
#    class DerivedClassName(Base1, Base2, Base3):

# fridge_on_time:
#  thread:
#    with lock:
#        timing = active
#    __on()
#    sleep(60)
#    __off()
#    sleep(90)
#    with lock:
#         timing = non_active


# in  on(), off()
#  ...
#  if (active): pass





        rrd_data     = "N:{:.2f}".format(measurements[DS_TEMP1].last()) + \
                        ":{:.2f}".format(measurements[DS_TEMPCPU].last()) + \
                        ":{:.2f}".format(measurements[DS_TEMP2].last()) + \
                        ":{:.2f}".format(measurements[DS_HUMI].last()) + \
                        ":{:}".format(fridge.status())    + \
                        ":{:}".format(reedcontact.status_stretched())
        print strftime("%H:%M:%S", localtime()), rrd_data
        rrdtool.update(RRDFILE, "--template", rrd_template, rrd_data)

        writeMonitoringData(rrd_data)

        sleep(35)



###############################################################################
# Exit ########################################################################
def _exit():
    """cleanup stuff"""
    fridge.cleanup()
    reedcontact.stop()
    reedcontact.join()
    sys.exit()

def __exit(__s, __f):
    """cleanup stuff used for signal handler"""
    _exit()



###############################################################################
###############################################################################
signal.signal(signal.SIGTERM, __exit)

try:
    main()

except KeyboardInterrupt:
    _exit()

except SystemExit:                  # Done in signal handler (method _exit()) #
    pass

except:
    print(traceback.print_exc())
    _exit()

finally:        # All cleanup is done in KeyboardInterrupt or signal handler. #
    pass

### eof ###

