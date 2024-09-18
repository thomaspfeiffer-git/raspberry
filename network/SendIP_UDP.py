#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# TODO                                                                        #
# (c) https://github.com/thomaspfeiffer-git 2024                              #
###############################################################################

"""
"""

"""
###### Usage ######
### Sensor
nohup ./SendIP_UDP.py --sender 2>&1 > sendip_udp.log &

### Receiver
nohup ./SendIP_UDP.py --receiver 2>&1 > sendip_udp.log &
"""


import argparse
import os
import socket
import subprocess
import sys
import time

sys.path.append("../libs/")
from Logging import Log
from Shutdown import Shutdown
import UDP


CREDENTIALS = os.path.expanduser("~/credentials/sendip_udp.cred")


###############################################################################
# IP ##########################################################################
class IP (object):
    dig = ['dig', '+short', 'txt', 'ch', 'whoami.cloudflare', '@1.0.0.1']
    def __init__ (self):
        self.udp = UDP.Sender(CREDENTIALS)

    def run (self):
        host = socket.gethostname()
        ip = subprocess.run(IP.dig, capture_output=True, text=True).stdout[:-1].replace('"', '')
        local_ip = subprocess.run(["hostname", "-I"], capture_output=True, text=True).stdout.rstrip()
        self.udp.send(f"{host}: {ip} (local: {local_ip})")


###############################################################################
# Receiver ####################################################################
class Receiver (object):
    def __init__ (self):
        self.udp = UDP.Receiver(CREDENTIALS)

    def run (self):
        while True:
            payload = self.udp.receive()


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
    shutdown_application = Shutdown(shutdown_func=shutdown_application)

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--sender", help="sends IP address to udp server", action="store_true")
    group.add_argument("--receiver", help="receives IP address from sender", action="store_true")
    args = parser.parse_args()

    if args.receiver:
        r = Receiver()
        r.run()

    if args.sender:
        ip = IP()
        ip.run()

# eof #

