#!/usr/bin/python
# -*- coding: utf-8 -*-
###############################################################################
# weather_draft_nano.py                                                       #
# (c) https://github.com/thomaspfeiffer-git 2016                              #
###############################################################################
"""Prepares a new weather.py running on a NanoPi NEO Air"""
"""(runs on a Raspberry Pi as well :-) )"""


import rrdtool
import signal
import sys
from threading import Lock
from time import sleep, strftime
import traceback

sys.path.append('../libs')
sys.path.append('../libs/sensors')

from Adafruit import Adafruit_GPIO_Platform as Platform
platform = Platform.platform_detect()

import BME280    # air pressure, temperature, humidity; indoor
import DS1820    # temperature
import HTU21DF   # temperature, humidity; outdoor
import CPU

from SensorQueue import SensorQueueClient_write
from SensorValue import SensorValueLock, SensorValue


# Misc for rrdtool
DATAFILE           = "/schild/weather/weather_nano.rrd"
DS_TEMPINDOOR      = "temp_indoor" 
DS_TEMPOUTDOOR     = "temp_outdoor"
DS_HUMIINDOOR      = "humi_indoor"
DS_HUMIOUTDOOR     = "humi_outdoor"
DS_REALTEMPOUTDOOR = "temp_3"
DS_TEMPINDOOR2     = "temp_4"
DS_AIRPRESSURE     = "air_pressure"
DS_TEMPCPU         = "temp_cpu"




###############################################################################
# Main ########################################################################
def main():
    """main part"""

    qvalue_temp_indoor      = SensorValueLock("ID_01_nano", "TempWohnzimmerIndoor", SensorValue.Types.Temp, u'°C', Lock())
    qvalue_humi_indoor      = SensorValueLock("ID_02_nano", "HumiWohnzimmerIndoor", SensorValue.Types.Humi, u'% rF', Lock())
    qvalue_temp_outdoor     = SensorValueLock("ID_03_nano", "TempWohnzimmerOutdoor", SensorValue.Types.Temp, u'°C', Lock())
    qvalue_humi_outdoor     = SensorValueLock("ID_04_nano", "HumiWohnzimmerOutdoor", SensorValue.Types.Humi, u'% rF', Lock())
    qvalue_pressure         = SensorValueLock("ID_05_nano", "Luftdruck", SensorValue.Types.Pressure, u'hPa', Lock())
    qvalue_temp_realoutdoor = SensorValueLock("ID_12_nano", "TempRealOutdoor", SensorValue.Types.Temp, u'°C', Lock())
    qvalue_temp_indoor2     = SensorValueLock("ID_13_nano", "TempWohnzimmerFenster", SensorValue.Types.Temp, u'°C', Lock())

    sq.register(qvalue_temp_indoor)
    sq.register(qvalue_humi_indoor)
    sq.register(qvalue_temp_outdoor)
    sq.register(qvalue_humi_outdoor)
    sq.register(qvalue_pressure)
    sq.register(qvalue_temp_realoutdoor)
    sq.register(qvalue_temp_indoor2)
    sq.start()

    bme280   = BME280.BME280(qvalue_pressure=qvalue_pressure, \
                             qvalue_temp=qvalue_temp_indoor,  \
                             qvalue_humi=qvalue_humi_indoor)
    global ds1820_1
    ds1820_1 = DS1820.DS1820("/sys/bus/w1/devices/28-000006b50d05/w1_slave", qvalue_temp_realoutdoor)
    ds1820_2 = DS1820.DS1820("/sys/bus/w1/devices/28-000006b575fb/w1_slave", qvalue_temp_indoor2)
    ds1820_3 = DS1820.DS1820("/sys/bus/w1/devices/28-000006b58b12/w1_slave")
    htu21df  = HTU21DF.HTU21DF(qvalue_temp=qvalue_temp_outdoor, qvalue_humi=qvalue_humi_outdoor)
    cpu      = CPU.CPU()

    rrd_template    = DS_TEMPINDOOR      + ":" + \
                      DS_TEMPOUTDOOR     + ":" + \
                      DS_HUMIINDOOR      + ":" + \
                      DS_HUMIOUTDOOR     + ":" + \
                      DS_REALTEMPOUTDOOR + ":" + \
                      DS_TEMPINDOOR2     + ":" + \
                      DS_AIRPRESSURE     + ":" + \
                      DS_TEMPCPU


    while True:
        bme280_pressure     = bme280.read_pressure()/100.0   # indoor #
        bme280_temperature  = bme280.read_temperature()
        bme280_humidity     = bme280.read_humidity()
        if platform == Platform.NANOPI:
            ds1820_1.consume_cpu_start()
        ds1820_1_temperature = ds1820_1.read_temperature()
        ds1820_2_temperature = ds1820_2.read_temperature()
        ds1820_3_temperature = ds1820_3.read_temperature()
        if platform == Platform.NANOPI:
            ds1820_1.consume_cpu_stop()
        htu21df_temperature = htu21df.read_temperature()     # outdoor #
        htu21df_humidity    = htu21df.read_humidity()
        cpu_temp            = cpu.read_temperature()
     
        rrd_data = "N:" + \
                   ":".join("{:.2f}".format(d) for d in [bme280_temperature,   \
                                                         htu21df_temperature,  \
                                                         bme280_humidity,      \
                                                         htu21df_humidity,     \
                                                         ds1820_1_temperature, \
                                                         ds1820_2_temperature, \
                                                         bme280_temperature,   \
                                                         cpu_temp])
                                                          
        print(strftime("%Y%m%d %X:"), rrd_data)
        rrdtool.update(DATAFILE, "--template", rrd_template, rrd_data) 
   
        sleep(45)


###############################################################################
# Exit ########################################################################
def _exit():
    """cleanup stuff"""
    sq.stop()
    sq.join()
    if platform == Platform.NANOPI:
        ds1820_1.consume_cpu_stop()
    sys.exit()

def __exit(__s, __f):
    """cleanup stuff used for signal handler"""
    _exit()


###############################################################################
###############################################################################
if __name__ == '__main__':
    signal.signal(signal.SIGTERM, __exit)

    try:
        ds1820_1 = None
        sq = SensorQueueClient_write()
        main()

    except KeyboardInterrupt:
        _exit()

    except SystemExit:              # Done in signal handler (method _exit()) #
        pass

    except:
        print(traceback.print_exc())
        _exit()

    finally:    # All cleanup is done in KeyboardInterrupt or signal handler. #
        pass

# eof #

