#!/usr/bin/python2

from time import sleep
from DHT22_AM2302 import DHT22_AM2302

DHT22_AM2302_PIN = 35


temphumi    = DHT22_AM2302(19)   # BCM 19 = PIN 35



while (True):
    _temp, _humi = temphumi.read()
    print "t:", _temp, "h:", _humi
    sleep(10)


