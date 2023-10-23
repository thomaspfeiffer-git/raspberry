#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# Receive_UDP_Data.py                                                         #
# (c) https://github.com/thomaspfeiffer-git 2023                              #
###############################################################################

"""
TODO
"""


"""
###### Usage ######
nohup ./Receive_UDP_Data.py 2>1 > receive_udp_data.log &
"""


import os
import sys

sys.path.append("../../libs/")
from Logging import Log
from Shutdown import Shutdown
import UDP


CREDENTIALS = os.path.expanduser("~/credentials/wardrobe_homeautomation.cred")


###############################################################################
# Receiver ####################################################################
class Receiver (object):
    def __init__ (self):
        self.udp = UDP.Receiver(CREDENTIALS)

    def start (self):
        while True:
            payload = self.udp.receive()
            try:
                source = payload.split(" - ")[0]
                data = payload.split(" - ")[1]
            except IndexError:
                Log("Wrong data format: {0[0]} {0[1]}".format(sys.exc_info()))
            else:
                Log(f"Source: {source}; Data: {data}")


###############################################################################
# Shutdown stuff ##############################################################
def shutdown_application ():
    """cleanup stuff"""
    Log("Stopping application")
    Log("Application stopped")
    sys.exit(0)


###############################################################################
## main #######################################################################
if __name__ == "__main__":
    r = Receiver()
    r.start()

# eof #

