#!/usr/bin/python
# -*- coding: utf-8 -*-
###############################################################################
# kollerberg_to_queue.py                                                      #
# Copies data from Kollerberg's data files to the queue used for the local    #
# weather station.                                                            #
# (c) https://github.com/thomaspfeiffer-git 2016                              #
###############################################################################


import signal
import sys
from time import sleep
import traceback


################################################################################
# Main #########################################################################
def Main():
    while True:
        # read data from files:
        #   ID_21: temp outdoor
        #   ID_22: humi outdoor
        #   ID_23: air pressure
        #   ID_24: temp indoor
        #   ID_25: humi indoor
        #   ID_26: temp basement
        #   ID_27: humi basement

        # write data into queue

        sleep 60



################################################################################
# Exit ########################################################################
def Exit():
    """cleanup stuff"""
    sys.exit()

def _Exit(__s, __f):
    """cleanup stuff used for signal handler"""
    Exit()


###############################################################################
###############################################################################
if __name__ == '__main__':
    signal.signal(signal.SIGTERM, _Exit)

    try:
        Main()

    except KeyboardInterrupt:
        Exit()

    except SystemExit:              # Done in signal handler (method _Exit()) #
        pass

    except:
        print(traceback.print_exc())

    finally:
        pass

# eof #
