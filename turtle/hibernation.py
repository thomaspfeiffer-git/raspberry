#!/usr/bin/python
# coding=utf-8
#############################################################################
#############################################################################

import signal
import sys
from time import sleep
import traceback

from DS1820 import DS1820


###############################################################################
# Main ########################################################################
def main():
    """main part"""
    temp_fridge = DS1820("/sys/bus/w1/devices/28-000006dc8d42/w1_slave")

    while (True):
        print temp_fridge.read()
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
signal.signal(signal.SIGTERM, __exit)

try:
    main()

except KeyboardInterrupt:
    _exit()

except SystemExit:                  # Done in signal handler (method _exit()) #
    pass

except:
    print(traceback.print_exc())
    _exit()

finally:        # All cleanup is done in KeyboardInterrupt or signal handler. #
    pass

### eof ###



