#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
#############################################################################
# weather.py                                                                #
# (c) https://github.com/thomaspfeiffer-git 2016, 2017, 2018                #
#############################################################################
"""Weather station at our summer cottage"""

### usage ###
# nohup ./weather.py &

import configparser as cfgparser
import datetime
import signal
import socket
import sys
from time import strftime, localtime, sleep, time
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

if this_PI == pik_i:   # BMP180 installed only at pik_i
    from sensors.BMP180 import BMP180


AddressesDS1820 = { pik_i: "/sys/bus/w1/devices/w1_bus_master1/28-000006de80e2/w1_slave",
                    pik_a: "/sys/bus/w1/devices/w1_bus_master1/28-000006dd6ac1/w1_slave",
                    pik_k: "/sys/bus/w1/devices/w1_bus_master1/28-000006de535b/w1_slave" }


DS_TEMP1 = "DS_TEMP1"
DS_TEMP2 = "DS_TEMP2"
DS_TCPU  = "DS_TCPU"
DS_HUMI  = "DS_HUMI"
DS_PRESS = "DS_PRESS"

DS = { pik_i: { DS_TEMP1: 'kb_i_t1', 
                DS_TEMP2: 'kb_i_t2',
                DS_TCPU : 'kb_i_tcpu',
                DS_HUMI : 'kb_i_humi',
                DS_PRESS: 'kb_i_press' },
       pik_a: { DS_TEMP1: 'kb_a_t1',
                DS_TEMP2: 'kb_a_t2',
                DS_TCPU : 'kb_a_tcpu',
                DS_HUMI : 'kb_a_humi',
                DS_PRESS: 'kb_a_press' },
       pik_k: { DS_TEMP1: 'kb_k_t1',
                DS_TEMP2: 'kb_k_t2',
                DS_TCPU : 'kb_k_tcpu',
                DS_HUMI : 'kb_k_humi',
                DS_PRESS: 'kb_k_press' }
     } 

DATAFILES = { pik_i: "/share/kb_i_weather",
              pik_a: "/share/kb_a_weather",
              pik_k: "/share/kb_k_weather" }



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
# writeData ###################################################################
def writeData(rrd_data):
    """write weather data to a file which is transferred to schild.smtp.at"""
    with open(DATAFILES[this_PI], 'w') as f:
        ts = time()
        f.write(datetime.datetime.fromtimestamp(ts).strftime("%Y%m%d%H%M%S:") + \
                str(ts) + ":" + rrd_data)


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
        print("wrong host!")
        _exit()

    udp = UDP_Sender()
    htu21df = HTU21DF()
    tempds  = DS1820(AddressesDS1820[this_PI])
    tempcpu = CPU()
    if this_PI == pik_i:
        bmp180 = BMP180()

    rrd_template = DS[this_PI][DS_TEMP1] + ":" + \
                   DS[this_PI][DS_TEMP2] + ":" + \
                   DS[this_PI][DS_TCPU]  + ":" + \
                   DS[this_PI][DS_HUMI]  + ":" + \
                   DS[this_PI][DS_PRESS]

    pressure = 1013.25 # in case of no BMP180 available
    while True:
        temp_ds  = tempds.read_temperature()
        temp_cpu = tempcpu.read_temperature()
        temp_htu = htu21df.read_temperature()
        humi_htu = htu21df.read_humidity()

        if this_PI == pik_i:
            pressure = bmp180.read_pressure() / 100.0

        rrd_data = "N:{:.2f}".format(temp_ds)     + \
                    ":{:.2f}".format(temp_htu)    + \
                    ":{:.2f}".format(temp_cpu)    + \
                    ":{:.2f}".format(humi_htu)    + \
                    ":{:.2f}".format(pressure)
        print(rrd_template)
        print("%s %s" % (strftime("%Y%m%d%H%M%S", localtime()), rrd_data))

        writeData(rrd_data)
        udp.send(rrd_data)

        sleep(45)


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
        print(traceback.print_exc())
        shutdown_application()

    finally:    # All cleanup is done in KeyboardInterrupt or signal handler. #
        pass

### eof ###

