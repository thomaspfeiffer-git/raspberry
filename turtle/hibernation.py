#!/usr/bin/python
# coding=utf-8
#############################################################################
#############################################################################

import rrdtool
import signal
import sys
from time import strftime, localtime, sleep
import traceback

from CPU import CPU
from DS1820 import DS1820
from Heating import Heating
from Measurements import Measurements


FRIDGE_PIN      = 38
FRIDGE_LATENCY  = 60 * 15


# Misc for rrdtool
RRDFILE     = "/schild/weather/hibernation.rrd"
DS_TEMP    = "hibernation_temp"
DS_TEMPCPU = "hibernation_tempcpu"
DS_HUMI    = "hibernation_humi"
DS_ON      = "hibernation_on"
DS_OPEN    = "hibernation_open"



fridge = Heating(FRIDGE_PIN, FRIDGE_LATENCY)


###############################################################################
# Main ########################################################################
def main():
    """main part"""
    temp_fridge = DS1820("/sys/bus/w1/devices/28-000006dc8d42/w1_slave")
    temp_cpu    = CPU()

    measurements = {DS_TEMP:    Measurements(), \
                    DS_TEMPCPU: Measurements(), \
                    DS_HUMI:    Measurements()}

    rrd_template = DS_TEMP    + ":" + \
                   DS_TEMPCPU + ":" + \
                   DS_HUMI    + ":" + \
                   DS_ON      + ":" + \
                   DS_OPEN

    while (True):
        measurements[DS_TEMP].append(temp_fridge.read())
        measurements[DS_TEMPCPU].append(temp_cpu.read())
        measurements[DS_HUMI].append(47)

        if (measurements[DS_TEMP].avg() > 6.0):
            fridge.on()
        if (measurements[DS_TEMP].avg() < 4.0):
            fridge.off()

        rrd_data     = "N:{:.2f}".format(measurements[DS_TEMP].last()) + \
                        ":{:.2f}".format(measurements[DS_TEMPCPU].last()) + \
                        ":{:.2f}".format(measurements[DS_HUMI].last()) + \
                        ":{:}".format(fridge.status())    + \
                        ":{:}".format(0)
        print strftime("%H:%M:%S", localtime()), rrd_data
        rrdtool.update(RRDFILE, "--template", rrd_template, rrd_data)

        sleep(40)



###############################################################################
# Exit ########################################################################
def _exit():
    """cleanup stuff"""
    fridge.cleanup()
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

