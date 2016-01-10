#!/usr/bin/python
# coding=utf-8
#############################################################################
# weather_kidsroom.py                                                       #
# Monitor temperature and humidity in our kid's room.                       #
# (c) https://github.com/thomaspfeiffer-git 2015                            #
#############################################################################
"""Monitor temperature and humidity in our kid's room."""

import datetime
import rrdtool
import signal
import sys
from time import strftime, localtime, sleep, time
import traceback

from CPU import CPU
from DHT22_AM2302 import DHT22_AM2302
from Measurements import Measurements


DHT22_AM2302_PIN = 35


# Misc for rrdtool
RRDFILE    = "/schild/weather/weather_kidsroom.rrd"
DS_TEMP1   = "kidsroom_temp1"
DS_TEMPCPU = "kidsroom_tempcpu"
DS_TEMP2   = "kidsroom_temp2"
DS_HUMI    = "kidsroom_humi"



###############################################################################
# Main ########################################################################
def main():
    """main part"""
    temphumi    = DHT22_AM2302(19)   # BCM 19 = PIN 35
    temp_cpu    = CPU()

    measurements = {DS_TEMP1:   Measurements(3), \
                    DS_TEMPCPU: Measurements(3), \
                    DS_TEMP2:   Measurements(3), \
                    DS_HUMI:    Measurements(3)}

    rrd_template = DS_TEMP1   + ":" + \
                   DS_TEMPCPU + ":" + \
                   DS_TEMP2   + ":" + \
                   DS_HUMI


    while (True):
        _temp, _humi = temphumi.read()
        measurements[DS_TEMP1].append(_temp)
        measurements[DS_HUMI].append(_humi)
        measurements[DS_TEMPCPU].append(temp_cpu.read())
        measurements[DS_TEMP2].append(0)   # empty, for later useage

        rrd_data     = "N:{:.2f}".format(measurements[DS_TEMP1].last()) + \
                        ":{:.2f}".format(measurements[DS_TEMPCPU].last()) + \
                        ":{:.2f}".format(measurements[DS_TEMP2].last()) + \
                        ":{:.2f}".format(measurements[DS_HUMI].last())
        print(strftime("%H:%M:%S", localtime()), rrd_data)
        rrdtool.update(RRDFILE, "--template", rrd_template, rrd_data)

        sleep(35)

###############################################################################
# Exit ########################################################################
def _exit():
    """cleanup stuff"""
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




