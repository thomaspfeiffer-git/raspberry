#!/usr/bin/python3
# -*- coding: utf-8 -*-
#############################################################################
# weather_kidsroom.py                                                       #
# Monitor temperature and humidity in our kid's room.                       #
# (c) https://github.com/thomaspfeiffer-git 2015, 2016, 2017                #
#############################################################################
"""Monitor temperature and humidity in our kid's room."""

# Start with:
# nohup sudo ./weather_kidsroom.py > /dev/null &

import datetime
import subprocess
import sys
from time import strftime, localtime, sleep, time

sys.path.append('../libs')
sys.path.append('../libs/sensors')
from CPU import CPU
from DHT22_AM2302 import DHT22_AM2302
from Measurements import Measurements
from SensorQueue2 import SensorQueueClient_write
from SensorValue2 import SensorValue, SensorValue_Data
from Shutdown import Shutdown

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
    sq = SensorQueueClient_write("../../configs/weatherqueue.ini")
    qvalue_temp = SensorValue("ID_06", "TempKinderzimmer", SensorValue_Data.Types.Temp, "°C")
    qvalue_humi = SensorValue("ID_07", "HumiKinderzimmer", SensorValue_Data.Types.Humi, "% rF")
    sq.register(qvalue_temp)
    sq.register(qvalue_humi)

    temphumi    = DHT22_AM2302(19, qvalue_temp, qvalue_humi)   # BCM 19 = PIN 35
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
        measurements[DS_TEMPCPU].append(temp_cpu.read_temperature())
        measurements[DS_TEMP2].append(0)   # empty, for later useage

        rrd_data = "N:{:.2f}".format(measurements[DS_TEMP1].last()) + \
                    ":{:.2f}".format(measurements[DS_TEMPCPU].last()) + \
                    ":{:.2f}".format(measurements[DS_TEMP2].last()) + \
                    ":{:.2f}".format(measurements[DS_HUMI].last())
        # print(strftime("%H:%M:%S", localtime()), rrd_data)
        # rrdtool.update(RRDFILE, "--template", rrd_template, rrd_data)

        # python rrdtool seems not to work here; the pi needs a proper reinstall.
        # as a workaround, i just call the os for rrd update
        # rrd = "/usr/bin/rrdtool update {} --template {} {}".format(RRDFILE, rrd_template, rrd_data)
        rrd = ["/usr/bin/rrdtool", "update", RRDFILE, "--template", rrd_template, rrd_data]
        print(rrd)
        subprocess.call(rrd)

        sleep(35)

###############################################################################
# Exit ########################################################################
def shutdown_application ():
    """cleanup stuff"""
    sys.exit(0)



###############################################################################
###############################################################################
if __name__ == '__main__':
    shutdown = Shutdown(shutdown_func=shutdown_application)

    main()

### eof ###

