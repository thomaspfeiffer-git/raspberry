#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
#############################################################################
# Kidsroom.py                                                               #
# Monitor temperature and humidity in our kid's room.                       #
# (c) https://github.com/thomaspfeiffer-git 2015, 2016, 2017, 2020          #
#############################################################################
"""Monitor temperature and humidity in our kid's room."""

# Start with:
# nohup sudo ./Kidsroom.py &

import configparser
import datetime
import os
import socket
import sys
from time import strftime, localtime, sleep, time

sys.path.append('../libs')
sys.path.append('../libs/sensors')
from Logging import Log
from CPU import CPU
from DHT22_AM2302 import DHT22_AM2302
from Measurements import Measurements
from SensorQueue2 import SensorQueueClient_write
from SensorValue2 import SensorValue, SensorValue_Data
from Shutdown import Shutdown

DHT22_AM2302_PIN = 35


# Misc for rrdtool
CREDENTIALS = os.path.expanduser("~/credentials/kidsroom.cred")
DS_TEMP1   = "kidsroom_temp1"
DS_TEMPCPU = "kidsroom_tempcpu"
DS_TEMP2   = "kidsroom_temp2"
DS_HUMI    = "kidsroom_humi"


###############################################################################
###############################################################################
class UDP (object):
    def __init__ (self, credentials_file):
        if not os.path.isfile(credentials_file):
            raise FileNotFoundError("File '{}' does not exist!".format(credentials_file))

        credentials = configparser.ConfigParser()
        credentials.read(credentials_file)

        self.SECRET = credentials['UDP']['SECRET']
        self.IP_ADDRESS_SERVER = credentials['UDP']['IP_ADDRESS_SERVER']
        self.UDP_PORT = int(credentials['UDP']['UDP_PORT'])
        self.MAX_PACKET_SIZE = int(credentials['UDP']['MAX_PACKET_SIZE'])


###############################################################################
###############################################################################
class Sender (UDP):
    def __init__ (self, credentials_file):
        super().__init__(credentials_file)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send (self, data):
        datagram = "{},no digest available here".format(data).encode('utf-8')
        try:
            sent = self.socket.sendto(datagram, (self.IP_ADDRESS_SERVER, self.UDP_PORT))
            Log("Sent bytes: {}; data: {}".format(sent, datagram))
        except:
            Log("Cannot send data: {0[0]} {0[1]} (Data: {1})".format(sys.exc_info(), datagram))


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
    udp = Sender(CREDENTIALS)

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
        # Log(rrd_data)
        udp.send(rrd_data)

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

