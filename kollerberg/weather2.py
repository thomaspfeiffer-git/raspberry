#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
#############################################################################
# weather.py                                                                #
# (c) https://github.com/thomaspfeiffer-git 2016, 2017, 2018, 2019          #
#############################################################################
"""Weather station at our summer cottage"""

### usage ###
# nohup ./weather.py 2>&1 > weather.log &

import configparser as cfgparser
import socket
import sys
import time
import traceback

sys.path.append('../libs')

from Commons import Digest
from Logging import Log
from Shutdown import Shutdown

from sensors.CPU import CPU
from sensors.HTU21DF import HTU21DF
from sensors.DS1820 import DS1820


# Hosts where this app runs
pik_i = "pik_i"
pik_a = "pik_a"
pik_k = "pik_k"
PIs = [pik_i, pik_a, pik_k]
this_PI = socket.gethostname()

if this_PI == pik_i:   # BME680 installed only at pik_i
    from sensors.BME680 import BME680, BME_680_SECONDARYADDR


AddressesDS1820 = { pik_i: "/sys/bus/w1/devices/w1_bus_master1/28-000006de80e2/w1_slave",
                    pik_a: "/sys/bus/w1/devices/w1_bus_master1/28-000006dd6ac1/w1_slave",
                    pik_k: "/sys/bus/w1/devices/w1_bus_master1/28-000006de535b/w1_slave" }


CREDENTIALS = "/home/pi/credentials/weather.cred"
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
            Log("Sent bytes: {}; data: {}".format(sent,datagram))
        except:
            Log("Cannot send data: {0[0]} {0[1]}".format(sys.exc_info()))


###############################################################################
# Main ########################################################################
def main():
    """main part"""

    if this_PI not in PIs:
        Log("wrong host!")
        shutdown_application()

    udp = UDP_Sender()
    tempds  = DS1820(AddressesDS1820[this_PI])
    tempcpu = CPU()
    if this_PI == pik_i:
        bme680  = BME680(i2c_addr=BME_680_SECONDARYADDR)
    else:
        htu21df = HTU21DF()

    pressure = 1013.25 # in case of no BME680 available
    airquality = 0

    while True:
        temp_ds  = tempds.read_temperature()
        temp_cpu = tempcpu.read_temperature()

        if this_PI == pik_i:
            temp = bme680.data.temperature
            humi = bme680.data.humidity
            pressure = bme680.data.pressure
            airquality = bme680.data.air_quality_score \
                         if bme680.data.air_quality_score != None else 0
            Log("Airquality: {}".format(airquality))             
        else:    
            temp = htu21df.read_temperature()
            humi = htu21df.read_humidity()

        rrd_data = "N:{:.2f}".format(temp_ds)     + \
                    ":{:.2f}".format(temp)    + \
                    ":{:.2f}".format(temp_cpu)    + \
                    ":{:.2f}".format(humi)    + \
                    ":{:.2f}".format(pressure)
                    # ":{:.2f}".format(airquality)

        udp.send("{},{}".format(this_PI,rrd_data))
        time.sleep(45)


###############################################################################
# shutdown ####################################################################
def shutdown_application ():
    """cleanup stuff"""
    Log("Stopping application")
    Log("Application stopped")
    sys.exit(0)


###############################################################################
# main ########################################################################
if __name__ == '__main__':
    shutdown_application = Shutdown(shutdown_func=shutdown_application)

    try:
        main()

    except KeyboardInterrupt:
        shutdown_application()

    except SystemExit:      # Done in signal handler (shutdown_application()) #
        pass

    except:
        Log(traceback.print_exc())
        shutdown_application()

    finally:    # All cleanup is done in KeyboardInterrupt or signal handler. #
        pass

### eof ###

