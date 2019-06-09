#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# Monitor.py                                                                  #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2019                   #
###############################################################################

"""
Monitoring some data on the seti hardware:
- CPU Load
- CPU Temperature

- Room temperature
- Room humidity
- Airflow temperature

- ... and some more
"""


### usage ###
# nohup ./Monitor.py 2>&1 > monitor.py &


### libraries to be installed ###
# sudo pip3 install psutil


import configparser as cfgparser
import os
import psutil
import socket
import sys
import time


sys.path.append("../libs/")
from Commons import Digest
from Logging import Log
from Shutdown import Shutdown

from sensors.CPU import CPU


# Hosts where this app runs
seti_01 = "seti_01"
seti_02 = "seti_02"
seti_03 = "seti_03"
seti_04 = "seti_04"
PIs = [seti_01, seti_02, seti_03, seti_04]
this_PI = socket.gethostname()


if this_PI == seti_01:
    from sensors.DS1820 import DS1820
    from sensors.HTU21DF import HTU21DF
    from actuators.SSD1306 import SSD1306

    from PIL import Image
    from PIL import ImageDraw
    from PIL import ImageFont


DS1820_Airflow = "/sys/bus/w1/devices/28-00000855fca3/w1_slave"
DS1820_Room    = "/sys/bus/w1/devices/28-000008386a83/w1_slave"


CREDENTIALS = "/home/pi/credentials/seti.cred"
cred = cfgparser.ConfigParser()
cred.read(CREDENTIALS)


###############################################################################
# CONFIG ######################################################################
class CONFIG (object):
    SECRET = cred['UDP']['SECRET']
    IP_ADDRESS_SERVER = cred['UDP']['IP_ADDRESS_SERVER']
    UDP_PORT = int(cred['UDP']['UDP_PORT'])
    MAX_PACKET_SIZE = int(cred['UDP']['MAX_PACKET_SIZE'])


###############################################################################
# UDP_Sender ##################################################################
class UDP_Sender (object):
    def __init__ (self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.digest = Digest(CONFIG.SECRET)

    def send (self, data):
        payload = data
        datagram = "{},{}".format(payload,self.digest(payload)).encode('utf-8')
        try:
            sent = self.socket.sendto(datagram, 
                                      (CONFIG.IP_ADDRESS_SERVER, 
                                      CONFIG.UDP_PORT))
            # Log("Sent bytes: {}; data: {}".format(sent,datagram))
        except:
            Log("Cannot send data: {0[0]} {0[1]}".format(sys.exc_info()))

###############################################################################
# Display #####################################################################
class Display (SSD1306):
    def __init__ (self):
        super().__init__()
        self.xpos = 4
        self.ypos = 4
        self.begin()
        self.clear()
        self.display()

        self.img = Image.new('1', (self.width, self.height))
        self.draw = ImageDraw.Draw(self.img)
        self.font = ImageFont.load_default()
        _, self.textheight = self.draw.textsize("Text", font=self.font)

    def show_data (self, temp_room, temp_airflow, humidity):
        self.draw.rectangle((0,0,self.width,self.height), outline=0, fill=255)
        y = self.ypos
        self.draw.text((self.xpos, y), "Zeit: {}".format(time.strftime("%X")), font=self.font, fill=0)
        y += self.textheight
        self.draw.text((self.xpos, y), "Temperatur: {:.1f} °C".format(temp_room), font=self.font, fill=0)
        y += self.textheight
        self.draw.text((self.xpos, y), "Temperatur: {:.1f} °C".format(temp_airflow), font=self.font, fill=0)
        y += self.textheight
        self.draw.text((self.xpos, y), "Luftf.: {:.1f} % rF".format(humidity), font=self.font, fill=0)

        self.image(self.img)
        self.display()


###############################################################################
## Shutdown stuff #############################################################
def shutdown_application ():
    """cleanup stuff"""
    Log("Stopping application")
    Log("Application stopped")
    sys.exit(0)


###############################################################################
## main #######################################################################
if __name__ == "__main__":
    shutdown_application = Shutdown(shutdown_func=shutdown_application)
    cpu = CPU()
    udp = UDP_Sender()

    if this_PI == seti_01:
        ds_room = DS1820(DS1820_Room)
        ds_airflow = DS1820(DS1820_Airflow)
        htu = HTU21DF()
        display = Display()

    temp_room    = -99.99 # in case no DS1820 available
    temp_airflow = -99.99
    humidity     = -99.99 # in case no HTU21DF available

    while True:
        cpu_usage = psutil.cpu_percent(percpu=True)
        
        if this_PI == seti_01:
            temp_room    = ds_room.read_temperature()
            temp_airflow = ds_airflow.read_temperature()
            humidity     = htu.read_humidity()
            display.show_data(temp_room, temp_airflow, humidity)

        rrd_data = "N:{:.2f}".format(cpu.read_temperature()) + \
                    ":{:.2f}".format(os.getloadavg()[0])     + \
                    ":{:.2f}".format(psutil.cpu_freq()[0])   + \
                    ":{:.2f}".format(cpu_usage[0])           + \
                    ":{:.2f}".format(cpu_usage[1])           + \
                    ":{:.2f}".format(cpu_usage[2])           + \
                    ":{:.2f}".format(cpu_usage[3])           + \
                    ":{:.2f}".format(temp_room)              + \
                    ":{:.2f}".format(temp_airflow)           + \
                    ":{:.2f}".format(humidity)               + \
                    ":{:.2f}".format(-99.04)   + \
                    ":{:.2f}".format(-99.05)   + \
                    ":{:.2f}".format(-99.06)
        # 99.04: reserved; maybe fan speed?
        # 99.05: reserved
        # 99.06: reserved

        udp.send("{},{}".format(this_PI,rrd_data))
        time.sleep(120)

# eof #        

