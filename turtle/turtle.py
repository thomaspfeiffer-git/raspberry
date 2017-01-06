#!/usr/bin/python
# -*- coding: utf-8 -*-
#############################################################################
# control of heat and light in our turtle's compound                        #
# (c) https://github.com/thomaspfeiffer-git 2015                            #
#############################################################################
"""control of heat and light in our turtle's compound"""

from collections import deque
import rrdtool
import signal
import sys
from threading import Lock
from time import strftime, localtime, sleep
import traceback


sys.path.append('../libs')
sys.path.append('../libs/sensors')

from CPU import CPU
from DHT22_AM2302 import DHT22_AM2302
from DS1820 import DS1820
from Heating import Heating
from Measurements import Measurements
import Schedules
from SensorQueue import SensorQueueClient_write
from SensorValue import SensorValueLock, SensorValue


HEATLAMP_PIN      = 38
HEATLAMP_LATENCY  = 60 * 15

LIGHTLAMP_PIN     = 36
LIGHTLAMP_LATENCY = 60 * 15


# Misc for rrdtool
RRDFILE     = "/schild/weather/turtle.rrd"
DS_TEMP1    = "turtle_temp1"
DS_TEMP2    = "turtle_temp2"
DS_TEMP3    = "turtle_temp3"
DS_TEMP4    = "turtle_temp4"
DS_TEMPCPU  = "turtle_tempcpu"
DS_HUMI     = "turtle_humi"
DS_HEATING  = "turtle_heating"
DS_LIGHTING = "turtle_lighting"


heatlamp  = Heating(HEATLAMP_PIN, HEATLAMP_LATENCY)
lightlamp = Heating(LIGHTLAMP_PIN, LIGHTLAMP_LATENCY)



###############################################################################
# Exit ########################################################################
def _exit():
    """cleanup stuff"""
    sq.stop()
    sq.join()
    heatlamp.cleanup()
    lightlamp.cleanup()
    sys.exit()

def __exit(__s, __f):
    """cleanup stuff used for signal handler"""
    _exit()


###############################################################################
# Main ########################################################################
def main():
    """main part"""
    qvalue_tempbox     = SensorValueLock("ID_08", "TempDonutBox", SensorValue.Types.Temp, u'°C', Lock())
    qvalue_humi        = SensorValueLock("ID_09", "HumiDonut", SensorValue.Types.Humi, u'% rF', Lock())
    qvalue_tempoutdoor = SensorValueLock("ID_12", "TempDonutOutDoor", SensorValue.Types.Temp, u'°C', Lock())
    qvalue_heatlamp    = SensorValueLock("ID_10", "SwitchHeatlamp", SensorValue.Types.Switch, u'Heizung:', Lock())
    qvalue_lightlamp   = SensorValueLock("ID_11", "SwitchLightlamp", SensorValue.Types.Switch, u'Beleuchtung:', Lock())
    sq.register(qvalue_tempbox)
    sq.register(qvalue_humi)
    sq.register(qvalue_tempoutdoor)
    sq.register(qvalue_heatlamp)
    sq.register(qvalue_lightlamp)
    sq.start()

    temp1        = DS1820("/sys/bus/w1/devices/28-000006d62eb1/w1_slave", qvalue_tempoutdoor)
    temp2        = DS1820("/sys/bus/w1/devices/28-000006dd6ac1/w1_slave")
    temp4        = DS1820("/sys/bus/w1/devices/28-000006de535b/w1_slave")
    temphumi     = DHT22_AM2302(21, qvalue_tempbox, qvalue_humi) # BCM 21 = PIN 40
    tempcpu      = CPU()
    heatcontrol  = Schedules.Control(Schedules.ScheduleHeat(), heatlamp, qvalue_heatlamp)
    lightcontrol = Schedules.Control(Schedules.ScheduleLight(), lightlamp, qvalue_lightlamp)

    measurements = {DS_TEMP1:   Measurements(), \
                    DS_TEMP2:   Measurements(), \
                    DS_TEMP3:   Measurements(), \
                    DS_TEMP4:   Measurements(), \
                    DS_TEMPCPU: Measurements(), \
                    DS_HUMI:    Measurements()}
 
    rrd_template = DS_TEMP1   + ":" + \
                   DS_TEMP2   + ":" + \
                   DS_TEMP3   + ":" + \
                   DS_TEMP4   + ":" + \
                   DS_TEMPCPU + ":" + \
                   DS_HUMI    + ":" + \
                   DS_HEATING + ":" + \
                   DS_LIGHTING
                     
    while (True):
        measurements[DS_TEMP1].append(temp1.read_temperature())
        measurements[DS_TEMP2].append(temp2.read_temperature())
        measurements[DS_TEMP4].append(temp4.read_temperature())
        _temp3, _humi = temphumi.read()
        measurements[DS_TEMP3].append(_temp3)
        measurements[DS_HUMI].append(_humi)
        measurements[DS_TEMPCPU].append(tempcpu.read())

        heatcontrol.control(measurements[DS_TEMP3].avg())
        lightcontrol.control(measurements[DS_TEMP3].avg())
        
        rrd_data     = "N:{:.2f}".format(measurements[DS_TEMP1].last()) + \
                        ":{:.2f}".format(measurements[DS_TEMP2].last()) + \
                        ":{:.2f}".format(measurements[DS_TEMP3].last()) + \
                        ":{:.2f}".format(measurements[DS_TEMP4].last()) + \
                        ":{:.2f}".format(measurements[DS_TEMPCPU].last()) + \
                        ":{:.2f}".format(measurements[DS_HUMI].last()) + \
                        ":{:}".format(heatlamp.status())    + \
                        ":{:}".format(lightlamp.status())
        print strftime("%H:%M:%S", localtime()), rrd_data
        rrdtool.update(RRDFILE, "--template", rrd_template, rrd_data) 

        sleep(35)


###############################################################################
###############################################################################
if __name__ == '__main__':
    signal.signal(signal.SIGTERM, __exit)

    try:
        sq = SensorQueueClient_write()
        main()

    except KeyboardInterrupt:
        _exit()

    except SystemExit:              # Done in signal handler (method _Exit()) #
        pass

    except:
        print(traceback.print_exc())
        _exit()

    finally:    # All cleanup is done in KeyboardInterrupt or signal handler. #
        pass

### eof ###

