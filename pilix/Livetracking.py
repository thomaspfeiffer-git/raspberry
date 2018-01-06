#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# Livetracking.py                                                             #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2017, 2018             #
###############################################################################
"""
... TODO: add some useful comments here

This lib can be used:
- standalone as a receiver/server on UDP/Internet (command line: --receiver)
- standalone as a relais from LoRa to UDP/GSM     (command line: --relais)
- imported into another python program as a sender/client:
    . sender of telemetry data on UDP/GSM
    . sender of telemetry data on LoRa
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

from actuators.RFM9x import RFM9x
from actuators.RFM9x_constants import *

from config import CONFIG
from csv_fieldnames import *


LoRa_Cfg_Medium = { LR_Cfg_Reg1: BW_125KHZ | CODING_RATE_4_5,
                    LR_Cfg_Reg2: SPREADING_FACTOR_128CPS | RX_PAYLOAD_CRC_ON,
                    LR_Cfg_Reg3: MOBILE_NODE_MOBILE | AGC_AUTO_ON,
                    LR_Cfg_BW:   125.0 }

LoRa_Cfg_Telemetry = { LR_Cfg_Reg1: BW_41K7HZ | CODING_RATE_4_8,
                       LR_Cfg_Reg2: SPREADING_FACTOR_4096CPS | RX_PAYLOAD_CRC_ON,
                       LR_Cfg_Reg3: MOBILE_NODE_MOBILE | AGC_AUTO_ON,
                       LR_Cfg_BW:   41.7 }

LoRa_Cfg_Telemetry_Stable = { LR_Cfg_Reg1: BW_62K5HZ | CODING_RATE_4_8,
                              LR_Cfg_Reg2: SPREADING_FACTOR_4096CPS | RX_PAYLOAD_CRC_ON,
                              LR_Cfg_Reg3: MOBILE_NODE_MOBILE | AGC_AUTO_ON,
                              LR_Cfg_BW:   62.5 }

# LoRa_Cfg = LoRa_Cfg_Medium
LoRa_Cfg = LoRa_Cfg_Telemetry
# LoRa_Cfg = LoRa_Cfg_Telemetry_Stable




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
# Sender_UDP ##################################################################
class Sender_UDP (threading.Thread):
    """sends some GPS data (lon, lat, alt, timestamp, voltage)
       to a server using UDP on a GSM connection"""
    def __init__ (self):
        threading.Thread.__init__(self)
        self.digest = Digest(CONFIG.Livetracking.SECRET)
        self.data = None
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._running = True

    def setdata (self, data):
        self.data = data

    def run (self):
        interval = CONFIG.Livetracking.Interval_UDP_OnBattery
        while self._running:
            if self.data:
                interval = CONFIG.Livetracking.Interval_UDP_OnBattery \
                           if self.data[V_RunningOnBattery] \
                           else CONFIG.Livetracking.Interval_UDP_OnPowersupply
                payload = "{},{},{},{},{:.3f},{}".format(self.data[V_GPS_Time],
                                                         self.data[V_GPS_Lon],
                                                         self.data[V_GPS_Lat],
                                                         self.data[V_GPS_Alt],
                                                         self.data[V_Voltage],
                                                         "gsm")

                datagram = "{},{}".format(payload,self.digest(payload)).encode('utf-8')
                try:
                    Log("Sending bytes (UDP): {}".format(datagram))
                    sent = self.socket.sendto(datagram, 
                                              (CONFIG.Livetracking.IP_ADDRESS_SERVER,
                                               CONFIG.Livetracking.UDP_PORT))
                    Log("Sent bytes (UDP): {}; data: {}".format(sent,datagram))
                except:
                    Log("Cannot send data (UDP): {0[0]} {0[1]}".format(sys.exc_info()))

            for _ in range(interval * 10):
                if self._running:
                    time.sleep(0.1)

    def stop (self):
        self._running = False


###############################################################################
# Sender_LoRa #################################################################
class Sender_LoRa (threading.Thread):
    """sends some GPS data (lon, lat, alt, timestamp, voltage)
       to a server using LoRa"""

    def __init__ (self):
        threading.Thread.__init__(self)
        self.digest = Digest(CONFIG.Livetracking.SECRET)
        self.data = None
        self.rfm96w = RFM9x(config=LoRa_Cfg, 
                                   frequency=CONFIG.Livetracking.LoRa_Frequency,
                                   int_pin=CONFIG.Livetracking.LoRa_pinInterrupt,
                                   reset_pin=CONFIG.Livetracking.LoRa_pinReset)
        if not self.rfm96w.init():
            Log("Error: RFM96W not found!")  
            self.rfm96w.cleanup()    # TODO: show some message on SSD1306!
            sys.exit()
        else:
            Log("RFM96W LoRa mode ok!")
            self.rfm96w.set_tx_power(CONFIG.Livetracking.LoRa_TX_Power)

        self._running = True

    def setdata (self, data):
        self.data = data

    def run (self):
        interval = CONFIG.Livetracking.Interval_LoRa_OnBattery
        while self._running:
            if self.data:
                interval = CONFIG.Livetracking.Interval_LoRa_OnBattery \
                           if self.data[V_RunningOnBattery] \
                           else CONFIG.Livetracking.Interval_LoRa_OnPowersupply
                payload = "{},{},{},{},{:.3f},{}".format(self.data[V_GPS_Time],
                                                         self.data[V_GPS_Lon],
                                                         self.data[V_GPS_Lat],
                                                         self.data[V_GPS_Alt],
                                                         self.data[V_Voltage],
                                                         "lora")

                datagram = "{},{}".format(payload,self.digest(payload)).encode('utf-8')
                Log("Sending bytes (LoRa): {}".format(datagram))
                self.rfm96w.send(self.rfm96w.str_to_data(payload))
                self.rfm96w.wait_packet_sent()
                Log("Sent bytes (LoRa): {}".format(datagram))

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
        self.connect()

    def connect (self):
        self.connection = mc.connect(host="localhost",
                                     user=CONFIG.Livetracking.SQL_USER,
                                     passwd=CONFIG.Livetracking.SQL_PASSWORD,
                                     db="pilix")
        self.cursor = self.connection.cursor()

    def reconnect (self):
        Log("reconnecting")
        self.close()
        self.connect()
        Log("reconnected")

    def execute (self, sql_command):
        try:
            self.cursor.execute(sql_command)
            self.connection.commit()
        except:   
            Log("Cannot execute sql: {0[0]} {0[1]}".format(sys.exc_info()))
            self.reconnect()
            try:
                self.cursor.execute(sql_command)    # TODO improve code. DRY!
                self.connection.commit()
            except:    
                Log("Cannot re-execute sql: {0[0]} {0[1]}".format(sys.exc_info()))

    def close (self):
        self.cursor.close()
        self.connection.close()


###############################################################################
# Receiver_UDP ################################################################
class Receiver (object):
    def __init__ (self):
        self.digest = Digest(CONFIG.Livetracking.SECRET)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((CONFIG.Livetracking.IP_ADDRESS_SERVER, 
                          CONFIG.Livetracking.UDP_PORT))
        self._running = True

    def store (self, data):
        def float_ (string):
            try:
                i = float(string)
            except:
                i = -8888.8
            return i    

        (timestamp, lon, lat, alt, voltage, source) = data.split(',')
        lon = float_(lon)
        lat = float_(lat)
        alt = float_(alt)

        sql = """INSERT INTO telemetry (timestamp, source, lon, lat, alt, voltage)
                 VALUES ('{timestamp}', '{source}', {lon}, {lat}, {alt}, {voltage});"""
        sql = sql.format(timestamp=timestamp, source=source, lon=lon, lat=lat,
                         alt=alt, voltage=voltage)
        Log("SQL: {}".format(sql))
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
                    self.store(data=payload)
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

