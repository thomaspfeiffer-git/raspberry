#!/usr/bin/python

import sys

sys.path.append('../libs')
sys.path.append('../libs/sensors')

from DHT22_AM2302 import DHT22_AM2302

DHT22_AM2302_PIN = 14  # Pin 8


tempdht = DHT22_AM2302(DHT22_AM2302_PIN)


temp_dht, humi_dht = tempdht.read()

print "t:", temp_dht, "h:", humi_dht


