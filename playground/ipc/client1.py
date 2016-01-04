#!/usr/bin/python

from time import strftime, localtime, sleep
from threading import Lock

from SensorQueue import SensorQueueClient
from SensorValue import SensorValue, SensorValueLock



def Log (logstr):
    """improved log output"""
    print strftime("%Y%m%d %H:%M:%S", localtime()), logstr


class Sensor (object):   # eg DS1820
    def __init__ (self, sensorvalue=None):
        self.__sv = sensorvalue

    def read (self):
        value = 22.2
        if self.__sv is not None:
            self.__sv.value = value 
        return value



sv = SensorValueLock("TempWohnzimmer", "temp", Lock())
sq  = SensorQueueClient(sv)
sq.start()


i = 0
sensor = Sensor(sv)

while (True):
    value = sensor.read()
    Log("client1, value = sensor.read(): %s" % value)
    i += 1
    sleep(25)
