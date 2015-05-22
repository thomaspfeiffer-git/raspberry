#!/usr/bin/python
# coding=utf-8


import dhtreader
import os
import re
import RPi.GPIO as io
import time



################################################################################
# GetCPUTemperature ############################################################
def GetCPUTemperature():
   res = os.popen('vcgencmd measure_temp').readline()
   return(float(res.replace("temp=","").replace("'C\n","")))


################################################################################
def read_sensor(path):
  value = "U"
  try:
    f = open(path, "r")
    line = f.readline()
    if re.match(r"([0-9a-f]{2} ){9}: crc=[0-9a-f]{2} YES", line):
      line = f.readline()
      m = re.match(r"([0-9a-f]{2} ){9}t=([+-]?[0-9]+)", line)
      if m:
        value = str(float(m.group(2)) / 1000.0)
    f.close()
  except (IOError), e:
    print time.strftime("%x %X"), "Error reading", path, ": ", e
  return value

pathes = (
  "/sys/bus/w1/devices/28-000006b4eb31/w1_slave",
  "/sys/bus/w1/devices/28-000006b58b12/w1_slave"
)



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


for path in pathes:
  temp = read_sensor(path)
  print("Sensor {}: {}".format(path,temp))


print("Temp: {:.2f} °C".format(temp_outdoor))
print("Humi: {:.2f} %".format(humi_outdoor))

print("CPU: {:.2f} °C".format(GetCPUTemperature()))

