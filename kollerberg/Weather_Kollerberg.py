#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
#############################################################################
# Weather_Kollerberg.py                                                     #
# (c) https://github.com/thomaspfeiffer-git 2020                            #
#############################################################################
"""Weather station at our summer cottage"""

"""
###### usage #####
### read data from sensor and send to udp server
nohup ./Weather_Kollerberg.py --sensor 2>&1 >weather_kollerberg.log &

### receive data via udp and store in rrd database
nohup ./Weather_Kollerberg.py --receiver_rrd 2>&1 >weather_kollerberg_rrd.log &

### receive data via udp and send to homeautomation server
nohup ./Weather_Kollerberg.py --receiver_homeautomation 2>&1 >weather_kollerberg_homeautomation.log &
"""

import argparse
import os
import socket
import sys
import time

sys.path.append('../libs')

from sensors.CPU import CPU
from sensors.HTU21DF import HTU21DF
from sensors.DS1820 import DS1820

from Logging import Log
from SensorQueue2 import SensorQueueClient_write
from SensorValue2 import SensorValue, SensorValue_Data
from Shutdown import Shutdown
import UDP


# Hosts where this app runs as --sensor
pik_i = "pik-i"
pik_a = "pik-a"
pik_k = "pik-k"
PIs = [pik_i, pik_a, pik_k]
this_PI = socket.gethostname()

if this_PI == pik_i:   # BME680 installed only at pik_i
    from sensors.BME680 import BME680, BME_680_SECONDARYADDR


AddressesDS1820 = { pik_i: "/sys/bus/w1/devices/w1_bus_master1/28-000006de80e2/w1_slave",
                    pik_a: "/sys/bus/w1/devices/w1_bus_master1/28-000006dd6ac1/w1_slave",
                    pik_k: "/sys/bus/w1/devices/w1_bus_master1/28-000006de535b/w1_slave" }


# Misc for rrdtool and other config stuff
QUEUE_INI = os.path.expanduser("~/configs/weatherqueue.ini")
CREDENTIALS_RRD = os.path.expanduser("~/credentials/weather_kollerberg_rrd.cred")
CREDENTIALS_HA = os.path.expanduser("~/credentials/weather_kollerberg_ha.cred")
RRDFILE = os.path.expanduser("~/rrd/databases/weather_kollerberg.rrd")
DS_TEMP1 = "DS_TEMP1"
DS_TEMP2 = "DS_TEMP2"
DS_TCPU  = "DS_TCPU"
DS_HUMI  = "DS_HUMI"
DS_PRESS = "DS_PRESS"
DS_AIRQ  = "DS_AIRQ"


###############################################################################
# Sensor ######################################################################
def Sensor ():
    """reads data from sensor"""

    if this_PI not in PIs:
        Log("wrong host!")
        global shutdown_application
        shutdown_application()

    tempds  = DS1820(AddressesDS1820[this_PI])
    tempcpu = CPU()
    if this_PI == pik_i:
        bme680 = BME680(i2c_addr=BME_680_SECONDARYADDR)
    else:
        htu21df = HTU21DF()

    udp_rrd = UDP.Sender(CREDENTIALS_RRD)  # Server for all rrd stuff
    udp_ha = UDP.Sender(CREDENTIALS_HA)    # Display at home ("Homeautomation")

    pressure = 1013.25 # in case of no BME680 available
    airquality = 0

    while True:
        temp_ds  = tempds.read_temperature()
        temp_cpu = tempcpu.read_temperature()

        if this_PI == pik_i:
            bme680.get_sensor_data()
            temp = bme680.data.temperature
            humi = bme680.data.humidity
            pressure = bme680.data.pressure
            airquality = bme680.data.air_quality_score \
                         if bme680.data.air_quality_score != None else 0
        else:
            temp = htu21df.read_temperature()
            humi = htu21df.read_humidity()

        rrd_data = "N:{:.2f}".format(temp_ds)     + \
                    ":{:.2f}".format(temp)    + \
                    ":{:.2f}".format(temp_cpu)    + \
                    ":{:.2f}".format(humi)    + \
                    ":{:.2f}".format(pressure) + \
                    ":{:.2f}".format(airquality)

        udp_rrd.send(f"{this_PI},{rrd_data}")
        udp_ha.send(f"{this_PI},{rrd_data}")
        time.sleep(45)


###############################################################################
# Receiver_RRD ################################################################
class Receiver_RRD (object):
    def __init__ (self):
        self.udp = UDP.Receiver(CREDENTIALS_RRD)
        self.data = { p: None for p in PIs }
        self.DS = { pik_i: { DS_TEMP1: 'kb_i_t1',
                             DS_TEMP2: 'kb_i_t2',
                             DS_TCPU : 'kb_i_tcpu',
                             DS_HUMI : 'kb_i_humi',
                             DS_PRESS: 'kb_i_press',
                             DS_AIRQ:  'kb_i_airquality' },
                    pik_a: { DS_TEMP1: 'kb_a_t1',
                             DS_TEMP2: 'kb_a_t2',
                             DS_TCPU : 'kb_a_tcpu',
                             DS_HUMI : 'kb_a_humi',
                             DS_PRESS: 'kb_a_press',
                             DS_AIRQ:  'kb_a_airquality' },
                    pik_k: { DS_TEMP1: 'kb_k_t1',
                             DS_TEMP2: 'kb_k_t2',
                             DS_TCPU : 'kb_k_tcpu',
                             DS_HUMI : 'kb_k_humi',
                             DS_PRESS: 'kb_k_press',
                             DS_AIRQ:  'kb_k_airquality' }
                  }

    def process (self):
        import rrdtool

        data_complete = True
        rrd_template = ""
        rrd_data = "N:"

        for p in PIs:
            if not self.data[p]:
                data_complete = False
            else:
                rrd_template += self.DS[p][DS_TEMP1] + ":" + \
                                self.DS[p][DS_TEMP2] + ":" + \
                                self.DS[p][DS_TCPU]  + ":" + \
                                self.DS[p][DS_HUMI]  + ":" + \
                                self.DS[p][DS_PRESS] + ":" + \
                                self.DS[p][DS_AIRQ] + ":"
                rrd_data += self.data[p].split("N:")[1].rstrip() + ":"

        if data_complete:
            rrd_template = rrd_template.rstrip(":")
            rrd_data     = rrd_data.rstrip(":")
            try:
                Log(f"Update RRD database: {rrd_data}")
                rrdtool.update(RRDFILE, "--template", rrd_template, rrd_data)
            except rrdtool.OperationalError:
                Log("Cannot update rrd database: {0[0]} {0[1]}".format(sys.exc_info()))

    def run (self):
        while True:
            payload = self.udp.receive()
            Log(f"Data received: {payload}")
            (source, values) = payload.split(',')
            # data[pik_k] = "N:10.00:10.00:10.00:10.00:1013.25:0.00"
            self.data[source] = values
            # Log("Data: {}".format(self.data))
            self.process()


###############################################################################
# Receiver_Homeautomation #####################################################
class Receiver_Homeautomation (object):
    def __init__ (self):
        self.udp = UDP.Receiver(CREDENTIALS_HA)
        self.data = { p: None for p in PIs }

        self.sq = SensorQueueClient_write(QUEUE_INI)
        self.qv_kb_i_t = SensorValue("ID_21", "Temp KB indoor", SensorValue_Data.Types.Temp, "°C")
        self.qv_kb_i_h = SensorValue("ID_22", "Humi KB indoor", SensorValue_Data.Types.Humi, "% rF")
        self.qv_kb_p   = SensorValue("ID_23", "Pressure KB",    SensorValue_Data.Types.Pressure, "hPa")

        self.qv_kb_a_t = SensorValue("ID_24", "Temp KB outdoor", SensorValue_Data.Types.Temp, "°C")
        self.qv_kb_a_h = SensorValue("ID_25", "Humi KB outdoor", SensorValue_Data.Types.Humi, "% rF")

        self.qv_kb_k_t = SensorValue("ID_26", "Temp KB basement", SensorValue_Data.Types.Temp, "°C")
        self.qv_kb_k_h = SensorValue("ID_27", "Humi KB basement", SensorValue_Data.Types.Humi, "% rF")

        self.sq.register(self.qv_kb_i_t)
        self.sq.register(self.qv_kb_i_h)
        self.sq.register(self.qv_kb_p)
        self.sq.register(self.qv_kb_a_t)
        self.sq.register(self.qv_kb_a_h)
        self.sq.register(self.qv_kb_k_t)
        self.sq.register(self.qv_kb_k_h)

    def process (self):
        if self.data[pik_i] is not None:
            self.qv_kb_i_t.value = "{:.1f}".format(float(self.data[pik_i].split(':')[1]))
            self.qv_kb_i_h.value = "{:.1f}".format(float(self.data[pik_i].split(':')[4]))
            self.qv_kb_p.value   = "{:.1f}".format(float(self.data[pik_i].split(':')[5]))
        if self.data[pik_a] is not None:
            self.qv_kb_a_t.value = "{:.1f}".format(float(self.data[pik_a].split(':')[1]))
            self.qv_kb_a_h.value = "{:.1f}".format(float(self.data[pik_a].split(':')[4]))
        if self.data[pik_k] is not None:
            self.qv_kb_k_t.value = "{:.1f}".format(float(self.data[pik_k].split(':')[1]))
            self.qv_kb_k_h.value = "{:.1f}".format(float(self.data[pik_k].split(':')[4]))

    def run (self):
        while True:
            payload = self.udp.receive()
            Log(f"Data received: {payload}")
            (source, values) = payload.split(',')
            self.data[source] = values
            self.process()


###############################################################################
# Exit ########################################################################
def shutdown_application ():
    """cleanup stuff"""
    Log("Stopping application")
    Log("Application stopped")
    sys.exit(0)


###############################################################################
# main ########################################################################
if __name__ == '__main__':
    shutdown_application = Shutdown(shutdown_func=shutdown_application)

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--sensor", help="read data from sensor and send to udp server", action="store_true")
    group.add_argument("--receiver_rrd", help="receive data via udp and store in rrd database", action="store_true")
    group.add_argument("--receiver_homeautomation", help="receive data via udp and send to homeautomation server", action="store_true")
    args = parser.parse_args()

    if args.sensor:
        Sensor()
    if args.receiver_rrd:
        r = Receiver_RRD()
        r.run()
    if args.receiver_homeautomation:
        r = Receiver_Homeautomation()
        r.run()

# eof #

