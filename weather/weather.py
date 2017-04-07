#!/usr/bin/python3
# -*- coding: utf-8 -*-
###############################################################################
# weather.py                                                                  #
# Monitors temperature, humidity, and air pressure in our living room         #
# and outside.                                                                #
# (c) https://github.com/thomaspfeiffer-git 2016, 2017                        #
###############################################################################
"""this new version runs on a NanoPi NEO Air"""
"""(runs on a Raspberry Pi as well :-) )"""

# start with:
# nohup ./weather.py 2>weather.err >weather.err &

import rrdtool
import sys
from time import sleep, strftime

sys.path.append('../libs')
sys.path.append('../libs/sensors')

from Adafruit import Adafruit_GPIO_Platform as Platform
platform = Platform.platform_detect()

import BME280    # air pressure, temperature, humidity; indoor
import DS1820    # temperature
import HTU21DF   # temperature, humidity; outdoor
import CPU

from SensorQueue2 import SensorQueueClient_write
from SensorValue2 import SensorValue, SensorValue_Data
from Shutdown import Shutdown


# Misc for rrdtool
DATAFILE           = "/schild/weather/weather.rrd"
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

    qvalue_temp_indoor      = SensorValue("ID_01", "TempWohnzimmerIndoor", SensorValue_Data.Types.Temp, "°C")
    qvalue_humi_indoor      = SensorValue("ID_02", "HumiWohnzimmerIndoor", SensorValue_Data.Types.Humi, "% rF")
    qvalue_temp_outdoor     = SensorValue("ID_03", "TempWohnzimmerOutdoor", SensorValue_Data.Types.Temp, "°C")
    qvalue_humi_outdoor     = SensorValue("ID_04", "HumiWohnzimmerOutdoor", SensorValue_Data.Types.Humi, "% rF")
    qvalue_pressure         = SensorValue("ID_05", "Luftdruck", SensorValue_Data.Types.Pressure, "hPa")
    qvalue_temp_realoutdoor = SensorValue("ID_12", "TempRealOutdoor", SensorValue_Data.Types.Temp, "°C")
    qvalue_temp_indoor2     = SensorValue("ID_13", "TempWohnzimmerFenster", SensorValue_Data.Types.Temp, "°C")

    sq.register(qvalue_temp_indoor)
    sq.register(qvalue_humi_indoor)
    sq.register(qvalue_temp_outdoor)
    sq.register(qvalue_humi_outdoor)
    sq.register(qvalue_pressure)
    sq.register(qvalue_temp_realoutdoor)
    sq.register(qvalue_temp_indoor2)

    bme280   = BME280.BME280(qvalue_pressure=qvalue_pressure, \
                             qvalue_temp=qvalue_temp_indoor,  \
                             qvalue_humi=qvalue_humi_indoor)
    global ds1820_1
    ds1820_1 = DS1820.DS1820("/sys/bus/w1/devices/28-000006d62eb1/w1_slave", qvalue_temp_realoutdoor)
    ds1820_2 = DS1820.DS1820("/sys/bus/w1/devices/28-000006dc8d42/w1_slave", qvalue_temp_indoor2)
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
                                                         bme280_pressure,   \
                                                         cpu_temp])
                                                          
        print(rrd_template)
        print(strftime("%Y%m%d %X:"), rrd_data)
        rrdtool.update(DATAFILE, "--template", rrd_template, rrd_data) 
   
        sleep(45)


###############################################################################
# Exit ########################################################################
def shutdown_application ():
    """cleanup stuff"""
    print("in _exit()")
    if platform == Platform.NANOPI:
        print("calling ds1820_1.consume_cpu_stop()")
        ds1820_1.consume_cpu_stop()
    sys.exit(0)


###############################################################################
###############################################################################
if __name__ == '__main__':
    shutdown = Shutdown(shutdown_func=shutdown_application)

    ds1820_1 = None
    sq = SensorQueueClient_write("../../configs/weatherqueue.ini")
    main()

# eof #

