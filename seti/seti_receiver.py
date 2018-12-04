#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
#                                                                             #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2018                   #
###############################################################################
"""
"""

### usage ####
# 


import configparser as cfgparser
import socket
import sys
import threading
import time

sys.path.append('../libs')

from Commons import Digest
from Logging import Log
from Shutdown import Shutdown

CREDENTIALS = "/home/pi/configs/seti.cred"


###############################################################################
# UDP_Receiver ################################################################
class UDP_Receiver (threading.Thread):
    def __init__ (self):
        threading.Thread.__init__(self)

        cred = cfgparser.ConfigParser()
        cred.read(CREDENTIALS)

        self.SECRET = cred['UDP']['SECRET']
        self.UDP_PORT = int(cred['UDP']['UDP_PORT'])
        self.MAX_PACKET_SIZE = int(cred['UDP']['MAX_PACKET_SIZE'])

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.my_ip(), self.UDP_PORT))
        self.socket.setblocking(False)
        self.digest = Digest(self.SECRET)

        self._running = True

    @staticmethod
    def my_ip ():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except:
            IP = '127.0.0.1'
        finally:
            s.close()
            return IP

    def process_data (self, datagram):
        (payload, digest_received) = datagram.rsplit(',', 1)
        # TODO: verify digest
        (source, values) = payload.split(',')
        # data[source] = values
        # Log("Data: {}".format(data))

    def run (self):
        while self._running:
            try:
                datagram = self.socket.recv(self.MAX_PACKET_SIZE).decode('utf-8')
                Log("Received: {}".format(datagram))
                self.process_data(datagram)
            except BlockingIOError:
                for _ in range(50):  # interruptible sleep
                    if not self._running:
                        break
                    time.sleep(0.1)

    def stop (self):
        self._running = False


###############################################################################
# shutdown ####################################################################
def shutdown_application ():
    """cleanup stuff"""
    Log("Stopping application")
    udp.stop()
    udp.join()
    Log("Application stopped")
    sys.exit(0)


###############################################################################
# main ########################################################################
if __name__ == '__main__':
    shutdown_app = Shutdown(shutdown_func=shutdown_application)

    udp = UDP_Receiver()
    udp.start()

    while True:
        time.sleep(120)

# eof #

