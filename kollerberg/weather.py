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


# Datenstruktur fuer diverse Namen, zB in der rrd erstellen

###############################################################################
# Main ########################################################################
def main():
    """main part"""

    this_PI = gethostname()

    if this_PI not in PIs:
        print("falscher host!")




###############################################################################
# Exit ########################################################################
def _exit():
    """cleanup stuff"""
    fridge.cleanup()
    reedcontact.stop()
    reedcontact.join()
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

