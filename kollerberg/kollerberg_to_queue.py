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
    print "Main"



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
