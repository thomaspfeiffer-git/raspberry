#!/usr/bin/python
# coding=utf-8


import dhtreader
import os
import RPi.GPIO as io
import time

from DS1820 import DS1820



################################################################################
# GetCPUTemperature ############################################################
def GetCPUTemperature():
   res = os.popen('vcgencmd measure_temp').readline()
   return(float(res.replace("temp=","").replace("'C\n","")))




t1 = DS1820("/sys/bus/w1/devices/28-000006b4eb31/w1_slave")
t2 = DS1820("/sys/bus/w1/devices/28-000006b58b12/w1_slave")


# DHT22/AM2302 (humidity, temperature)
pin_sensor_outdoor     = 40
pin_sensor_outdoor_bcm = 21

dhtreader.init()


################################################################################
# IO für Relais ################################################################

io.setmode(io.BOARD)
io.setup(38,io.OUT)
#io.output(38,io.HIGH)
#time.sleep(2)
#io.output(38,io.LOW)
io.cleanup()


temp_outdoor, humi_outdoor = dhtreader.read(22,pin_sensor_outdoor_bcm)


print t1.read()
print t2.read()


print("Temp: {:.2f} °C".format(temp_outdoor))
print("Humi: {:.2f} %".format(humi_outdoor))

print("CPU: {:.2f} °C".format(GetCPUTemperature()))

