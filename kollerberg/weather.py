#!/usr/bin/python
# -*- coding: utf-8 -*-
#############################################################################
# hibernation.py                                                            #
# (c) https://github.com/thomaspfeiffer-git 2016                            #
#############################################################################
"""Weather station at our summer cottage"""

import datetime
import rrdtool
import signal
from socket import gethostname
import sys
from time import strftime, localtime, sleep, time
import traceback

sys.path.append('../libs')
sys.path.append('../libs/sensors')

from CPU import CPU
from DHT22_AM2302 import DHT22_AM2302
from DS1820 import DS1820


# Hosts where this app runs
pik_i = "pik_i"
pik_a = "pik_a"
pik_k = "pik_k"
PIs = [pik_i, pik_a, pik_k]
this_PI = gethostname()

if this_PI == pik_i:   # BMP085 installed only at pik_i
    from BMP085 import BMP085


AddressesDS1820 = { pik_i: "/sys/bus/w1/devices/w1_bus_master1/28-000006de80e2/w1_slave",
                    pik_a: "/sys/bus/w1/devices/w1_bus_master1/28-000006dd6ac1/w1_slave",
                    pik_k: "" }

DHT22_AM2302_PIN = 14


# Misc for rrdtool
RRDFILE    = "/share/weather_kollerberg.rrd"

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

DATAFILES = { pik_i: "/share/kb_i_weather.data",
              pik_a: "/share/kb_a_weather.data",
              pik_k: "/share/kb_k_weather.data" }


###############################################################################
# writeData ###################################################################
def writeData(rrd_data):
    """write various data to a file which is transferred to schild.smtp.at with crontab"""
    with open(DATAFILES[this_PI], 'w') as f:
        ts = time()
        f.write(datetime.datetime.fromtimestamp(ts).strftime("%Y%m%d%H%M%S:") + str(ts) + ":" + rrd_data)



###############################################################################
# Main ########################################################################
def main():
    """main part"""

    if this_PI not in PIs:
        print("wrong host!")
        _exit()

    tempdht = DHT22_AM2302(DHT22_AM2302_PIN)
    tempds  = DS1820(AddressesDS1820[this_PI])
    tempcpu = CPU()
    if this_PI == pik_i:
        bmp085 = BMP085()

    rrd_template = DS[this_PI][DS_TEMP1] + ":" + \
                   DS[this_PI][DS_TEMP2] + ":" + \
                   DS[this_PI][DS_TCPU]  + ":" + \
                   DS[this_PI][DS_HUMI]  + ":" + \
                   DS[this_PI][DS_PRESS]

    pressure = 0.0 # in case of no BMP085 available
    while True:
        temp_ds           = tempds.read()
        temp_cpu          = tempcpu.read()
        temp_dht, humi_dht = tempdht.read()
        if this_PI == pik_i:
            pressure = bmp085.read() / 100.0

        rrd_data = "N:{:.2f}".format(temp_ds)     + \
                    ":{:.2f}".format(temp_dht)    + \
                    ":{:.2f}".format(temp_cpu)    + \
                    ":{:.2f}".format(humi_dht)    + \
                    ":{:.2f}".format(pressure)
        # rrdtool.update(DATAFILE, "--template", rrd_template, rrd_data) 
        print(rrd_template)
        print("%s %s" % (strftime("%Y%m%d%H%M%S", localtime()), rrd_data))

        writeData(rrd_data)

        sleep(30)


###############################################################################
# Exit ########################################################################
def _exit():
    """cleanup stuff"""
    sys.exit()

def __exit(__s, __f):
    """cleanup stuff used for signal handler"""
    _exit()



###############################################################################
###############################################################################
if __name__ == '__main__':
    signal.signal(signal.SIGTERM, __exit)

    try:
        main()

    except KeyboardInterrupt:
        _exit()

    except SystemExit:              # Done in signal handler (method _exit()) #
        pass

    except:
        print(traceback.print_exc())
        _exit()

    finally:    # All cleanup is done in KeyboardInterrupt or signal handler. #
        pass

### eof ###

