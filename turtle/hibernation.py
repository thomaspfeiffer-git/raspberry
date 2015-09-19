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
from DHT22_AM2302 import DHT22_AM2302
from DS1820 import DS1820
from Heating import Heating
from Measurements import Measurements
from Reedcontact import Reedcontact


DHT22_AM2302_PIN = 40

REEDCONTACT_PIN  = 38

FRIDGE_PIN       = 36
FRIDGE_LATENCY   = 60 * 15


# Misc for rrdtool
RRDFILE    = "/schild/weather/hibernation.rrd"
DS_TEMP1   = "hibernation_temp1"
DS_TEMPCPU = "hibernation_tempcpu"
DS_TEMP2   = "hibernation_temp2"
DS_HUMI    = "hibernation_humi"
DS_ON      = "hibernation_on"
DS_OPEN    = "hibernation_open"


fridge = Heating(FRIDGE_PIN, FRIDGE_LATENCY)
reedcontact = Reedcontact(REEDCONTACT_PIN)


###############################################################################
# Main ########################################################################
def main():
    """main part"""
    temp_fridge = DS1820("/sys/bus/w1/devices/28-000006dc8d42/w1_slave")
    temp_cpu    = CPU()
    temphumi    = DHT22_AM2302(21)   # BCM 21 = PIN 40

    measurements = {DS_TEMP1:   Measurements(), \
                    DS_TEMPCPU: Measurements(), \
                    DS_TEMP2:   Measurements(), \
                    DS_HUMI:    Measurements()}

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

        if (measurements[DS_TEMP1].avg() > 6.0):
            fridge.on()
        if (measurements[DS_TEMP1].avg() < 4.0):
            fridge.off()

        rrd_data     = "N:{:.2f}".format(measurements[DS_TEMP1].last()) + \
                        ":{:.2f}".format(measurements[DS_TEMPCPU].last()) + \
                        ":{:.2f}".format(measurements[DS_TEMP2].last()) + \
                        ":{:.2f}".format(measurements[DS_HUMI].last()) + \
                        ":{:}".format(fridge.status())    + \
                        ":{:}".format(reedcontact.status())
        print strftime("%H:%M:%S", localtime()), rrd_data
        rrdtool.update(RRDFILE, "--template", rrd_template, rrd_data)

        sleep(35)



###############################################################################
# Exit ########################################################################
def _exit():
    """cleanup stuff"""
    fridge.cleanup()
    reedcontact.cleanup()
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

