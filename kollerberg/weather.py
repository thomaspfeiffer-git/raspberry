#!/usr/bin/python
# -*- coding: utf-8 -*-
#############################################################################
# hibernation.py                                                            #
# (c) https://github.com/thomaspfeiffer-git 2016                            #
#############################################################################
"""Weather station at our summer cottage"""

import signal
from socket import gethostname
import sys
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
if this_PI == pik_i:
    from BMP085 import BMP085


AddressesDS1820 = { pik_i: "/sys/bus/w1/devices/w1_bus_master1/28-000006de80e2/w1_slave",
                    pik_a: "/sys/bus/w1/devices/w1_bus_master1/28-000006dd6ac1/w1_slave",
                    pik_k: "" }


DHT22_AM2302_PIN = 14
if this_PI == pik_i:
    bmp85  = BMP085()
dht22  = DHT22_AM2302(DHT22_AM2302_PIN)
ds1820 = DS1820(AddressesDS1820[this_PI])





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


###############################################################################
# Main ########################################################################
def main():
    """main part"""


    if this_PI not in PIs:
        print("falscher host!")

    if this_PI == pik_i:
        pressure = bmp85.read() / 100.0
        print("BMP85: %6.2f hPa" % pressure)

    temp22, humi22 = dht22.read()
    tempds = ds1820.read()

    print("DHT: %3.2f °C; %2.2f %% rF" % (temp22, humi22))
    print("DS1820: %3.2f °C" % tempds)


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

