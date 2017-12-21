#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# Livetracking.py                                                             #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2017                   #
###############################################################################
"""
...

This lib can be used standalone as a receiver/server and imported into
another python program as a sender/client.
"""


### usage ###
# nohup ./Livetracking.py >livetracking.log 2>&1 &


import base64
import hashlib
import hmac
import socket
import sys
import threading
import time

sys.path.append("../libs/")
from Logging import Log

from config import CONFIG
from csv_fieldnames import *


###############################################################################
# Digest ######################################################################
class Digest (object):
    def __init__ (self, secret):
        self.__secret = secret.encode('utf-8')

    def __call__ (self, data):
        digest_maker = hmac.new(self.__secret, 
                                data.encode('utf-8'), 
                                hashlib.sha256) 
        return base64.encodestring(digest_maker.digest()).decode('utf-8').rstrip()


###############################################################################
# Sender ######################################################################
class Sender (threading.Thread):
    """sends some GPS data (lon, lat, alt, timestamp, voltage)
       to a server using UDP"""
    def __init__ (self):
        threading.Thread.__init__(self)
        self.digest = Digest(CONFIG.Livetracking.SECRET)
        self.data = None
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._running = True

    def setdata (self, data):
        self.data = data

    def run (self):
        interval = CONFIG.Livetracking.Interval_OnBattery
        while self._running:
            if self.data:
                interval = CONFIG.Livetracking.Interval_OnBattery \
                           if self.data[V_RunningOnBattery] \
                           else CONFIG.Livetracking.Interval_OnPowersupply
                payload = "{},{},{},{},{}".format(self.data[V_GPS_Time],
                                                  self.data[V_GPS_Lon],
                                                  self.data[V_GPS_Lat],
                                                  self.data[V_GPS_Alt],
                                                  self.data[V_Voltage])

                datagram = "{},{}".format(payload,self.digest(payload)).encode('utf-8')
                try:
                    sent = self.socket.sendto(datagram, 
                                              (CONFIG.Livetracking.IP_ADDRESS_SERVER,
                                               CONFIG.Livetracking.UDP_PORT))
                    Log("sent bytes: {}; data: {}".format(sent,datagram))
                except:
                    Log("Cannot send data: {0[0]} {0[1]}".format(sys.exc_info()))

            for _ in range(interval * 10):
                if self._running:
                    time.sleep(0.1)

    def stop (self):
        self._running = False


###############################################################################
# Database ####################################################################
class Database (object):
    """
CREATE USER 'pilix'@'localhost' IDENTIFIED BY 'password';
CREATE DATABASE pilix;
GRANT ALL PRIVILEGES ON pilix.* to 'pilix'@'localhost';
FLUSH PRIVILEGES;

USE pilix;
CREATE TABLE telemetry (
    id BIGINT(20) PRIMARY KEY NOT NULL auto_increment,
    ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    timestamp VARCHAR(32) NOT NULL,
    source SET('gsm', 'lora'),
    lon FLOAT,
    lat FLOAT,
    alt FLOAT,
    voltage FLOAT,
    KEY timestamp (timestamp)
); 
    """

    def __init__ (self):
        self.connection = mc.connect(host="localhost",
                                     user=CONFIG.Livetracking.SQL_USER,
                                     passwd=CONFIG.Livetracking.SQL_PASSWORD,
                                     db="pilix")
        self.cursor = self.connection.cursor()

    def execute (self, sql_command):
        self.cursor.execute(sql_command)
        self.connection.commit()

    def close (self):
        self.cursor.close()
        self.connection.close()


###############################################################################
# Receiver ####################################################################
class Receiver (object):
    def __init__ (self):
        self.digest = Digest(CONFIG.Livetracking.SECRET)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((CONFIG.Livetracking.IP_ADDRESS_SERVER, 
                          CONFIG.Livetracking.UDP_PORT))
        self._running = True

    def store (self, source, data):
        def int_ (string):
            try:
                i = int(string)
            except:
                i = -8888.8
            return i    

        (timestamp, lon, lat, alt, voltage) = data.split(',')
        lon = int_(lon)
        lat = int_(lat)
        alt = int_(alt)

        sql = """INSERT INTO telemetry (timestamp, source, lon, lat, alt, voltage)
                 VALUES ('{timestamp}', '{source}', {lon}, {lat}, {alt}, {voltage});"""
        sql = sql.format(timestamp=timestamp, source=source, lon=lon, lat=lat,
                         alt=alt, voltage=voltage)
        db.execute(sql)

    def run (self):
        while self._running:
            try:
                datagram = self.socket.recv(CONFIG.Livetracking.MAX_PACKET_SIZE).decode('utf-8')
            except KeyboardInterrupt:
                self._running = False
            else:    
                (payload, digest_received) = datagram.rsplit(',', 1)
                if hmac.compare_digest(digest_received, self.digest(payload)):
                    Log("Received data: {}".format(datagram))
                    self.store(source='gsm', data=payload)
                else:
                    Log("Hashes do not match on data: {}".format(datagram))

        db.close()        

    def stop (self):
        self._running = False


###############################################################################
# shutdown ####################################################################
def shutdown_application ():
    """cleanup stuff"""
    Log("Stopping application")
    db.close() 
    Log("Application stopped")
    sys.exit(0)

###############################################################################
## main #######################################################################
if __name__ == "__main__":
    import mysql.connector as mc
    from Shutdown import Shutdown
    shutdown_application = Shutdown(shutdown_func=shutdown_application)

    db = Database()
    r = Receiver()
    r.run()

# eof #

