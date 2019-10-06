#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
##############################################################################
# check_network.py                                                           #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2019                  #
##############################################################################


"""
wlan0: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
ether b0:f1:ec:11:6b:20  txqueuelen 1000  (Ethernet)


wlan0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
inet 192.168.8.211  netmask 255.255.255.0  broadcast 192.168.8.255
inet6 fe80::5950:caa9:21f6:bcff  prefixlen 64  scopeid 0x20<link>
ether b0:f1:ec:11:6b:20  txqueuelen 1000  (Ethernet)



https://github.com/raspberrypi/linux/issues/2453
modprobe -r brcmfmac
modprobe brcmfmac

==> missing wlan0 in ifconfig

==> only reboot "fixed" it so far



some more usefull hints:
https://askubuntu.com/questions/271387/how-to-restart-wifi-connection




"""


import subprocess
import sys
import time

sys.path.append('../libs')

from Logging import Log
from Shutdown import Shutdown


###############################################################################
###############################################################################
def ping ():
    IP = "128.0.3.45"
    try:
        subprocess.check_call(["ping", "-c", "1", "-w", "1", IP], 
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False


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
    ping_fails = 0

    while True:
        if not ping():
            ping_fails += 1
            Log("Ping #{} failed.".format(ping_fails))
        else:
            ping_fails = 0


# eof #

