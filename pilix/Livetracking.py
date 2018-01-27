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
  nohup ./Livetracking.py --receiver >livetracking.log 2>&1 &
- standalone as a relais from LoRa to UDP/GSM     (command line: --relais)
  nohup ./Livetracking.py --relais >livetracking.log 2>&1 &
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

try:
    from actuators.RFM9x import RFM9x
except ImportError:
    """in case of no hardware present (receiver/server on UDP),
       we fake this class"""
    class RFM9x (object):
        pass

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
# Payload #####################################################################
class Payload (object):
    def __init__ (self, source):
        self.digest = Digest(CONFIG.Livetracking.SECRET)
        self.__data = None
        self.__source = source

    def __call__ (self):
        return self.data

    @property
    def data (self):
        if self.__data:
            payload = "{},{},{},{},{:.3f},{}".format(self.__data[V_GPS_Time],
                                                     self.__data[V_GPS_Lon],
                                                     self.__data[V_GPS_Lat],
                                                     self.__data[V_GPS_Alt],
                                                     self.__data[V_Voltage],
                                                     self.__source)
            payload = "{},{}".format(payload,self.digest(payload)).encode('utf-8')
            return payload
        else:
            return None

    @data.setter
    def data (self, data):
        self.__data = data


###############################################################################
# UDP #########################################################################
class UDP (object):
    def __init__ (self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send (self, datagram):
        try:
            Log("Sending bytes (UDP): {}".format(datagram))
            sent = self.socket.sendto(datagram, 
                                      (CONFIG.Livetracking.IP_ADDRESS_SERVER,
                                       CONFIG.Livetracking.UDP_PORT))
            Log("Sent bytes (UDP): {}; data: {}".format(sent,datagram))
        except:
            Log("Cannot send data (UDP): {0[0]} {0[1]}".format(sys.exc_info()))


###############################################################################
# Sender_UDP ##################################################################
class Sender_UDP (threading.Thread):
    """sends some GPS data (lon, lat, alt, timestamp, voltage)
       to a server using UDP on a GSM connection"""
    def __init__ (self):
        threading.Thread.__init__(self)
        self.payload = Payload(source="gsm")
        self.udp = UDP()
        self.runningonbattery = True
        self._running = True

    def setdata (self, data):
        self.payload.data = data
        self.runningonbattery = data[V_RunningOnBattery]

    def run (self):
        interval = CONFIG.Livetracking.Interval_UDP_OnBattery
        while self._running:
            datagram = self.payload()
            if datagram:
                interval = CONFIG.Livetracking.Interval_UDP_OnBattery \
                           if self.runningonbattery \
                           else CONFIG.Livetracking.Interval_UDP_OnPowersupply
                self.udp.send(datagram)           

            for _ in range(interval * 10):
                if self._running:
                    time.sleep(0.1)

    def stop (self):
        self._running = False


###############################################################################
# Pilix_RFM96W ################################################################
class Pilix_RFM96W (RFM9x):
    def __init__ (self, sender=True):
        super().__init__(config=LoRa_Cfg, 
                         frequency=CONFIG.Livetracking.LoRa_Frequency,
                         int_pin=CONFIG.Livetracking.LoRa_pinInterrupt,
                         reset_pin=CONFIG.Livetracking.LoRa_pinReset)
        if not self.init():
            Log("Error: RFM96W not found!")  
            self.cleanup()    # TODO: show some message on SSD1306!
            sys.exit()
        else:
            Log("RFM96W LoRa mode ok!")

        if sender:    
            # self.set_tx_power(CONFIG.Livetracking.LoRa_TX_Power)
            self.set_tx_power(PA_MAX_BOOST)
        else:    
            self.set_lna(LNA_BOOST_MAX)


###############################################################################
# Sender_LoRa #################################################################
class Sender_LoRa (threading.Thread):
    """sends some GPS data (lon, lat, alt, timestamp, voltage)
       to a server using LoRa"""

    def __init__ (self):
        threading.Thread.__init__(self)
        self.payload = Payload(source="lora")
        self.rfm96w = Pilix_RFM96W(sender=True)
        self.runningonbattery = True
        self._running = True

    def setdata (self, data):
        self.payload.data = data
        self.runningonbattery = data[V_RunningOnBattery]

    def run (self):
        interval = CONFIG.Livetracking.Interval_LoRa_OnBattery
        while self._running:
            datagram = self.payload()
            if datagram:
                interval = CONFIG.Livetracking.Interval_LoRa_OnBattery \
                           if self.runningonbattery \
                           else CONFIG.Livetracking.Interval_LoRa_OnPowersupply
                Log("Sending bytes (LoRa): {}".format(datagram))
                self.rfm96w.send(self.rfm96w.bytes_to_data(datagram))
                self.rfm96w.wait_packet_sent()
                Log("Sent bytes (LoRa): {}".format(datagram))

            for _ in range(interval * 10):
                if self._running:
                    time.sleep(0.1)

    def stop (self):
        self._running = False


###############################################################################
# Display #####################################################################
class Display (object):
    def __init__ (self):
        from actuators.SSD1306 import SSD1306

        from PIL import Image
        from PIL import ImageDraw
        from PIL import ImageFont

        self.display = SSD1306()
        self.display.begin()
        self.display.clear()
        self.display.display()

        self.xpos = 4
        self.ypos = 4
        self.width = self.display.width
        self.height = self.display.height
        self.image = Image.new('1', (self.width, self.height))
        self.draw = ImageDraw.Draw(self.image)
        self.font = ImageFont.load_default()
        (_, self.textheight) = self.draw.textsize("Text", font=self.font)

    def showdata (self, data, rssi):        
        (timestamp, lon, lat, alt, voltage, source, digest) = data.split(',')
        self.draw.rectangle((0,0,self.width,self.height), outline=0, fill=255)
        y = self.ypos
        self.draw.text((self.xpos, y), "{}".format(timestamp))
        y += self.textheight
        self.draw.text((self.xpos, y), "X: {}".format(lon))
        y += self.textheight
        self.draw.text((self.xpos, y), "Y: {}".format(lat))
        y += self.textheight
        self.draw.text((self.xpos, y), "Z: {}".format(alt))
        y += self.textheight
        self.draw.text((self.xpos, y), "V: {} RSSI: {} ".format(voltage, rssi))

        self.display.image(self.image)
        self.display.display()

    def close (self):    
        self.display.clear()
        self.display.display()


###############################################################################
# Ralais ######################################################################
class Relais (object):
    """receives LoRa data and forwards them to the server using UDP"""
    def __init__ (self):
        self.rfm96w  = Pilix_RFM96W(sender=False)
        self.udp     = UDP()
        self.display = Display()

        self._running = True

    def run (self):
        while self._running:
            while not self.rfm96w.available():
                pass
            
            data = self.rfm96w.recv()
            str = "".join(map(chr, data))
            Log("RFM96W: Data received: {}".format(str))
            rssi = self.rfm96w.last_rssi
            Log("RSSI: {}".format(rssi))
            self.udp.send(str.encode('utf-8'))
            self.display.showdata(str, rssi)

    def stop (self):
        self._running = False
        self.rfm96w.set_mode_idle()
        self.rfm96w.cleanup()
        self.display.close()


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
        self.db = Database()

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
        self.db.execute(sql)

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

    def stop (self):
        self._running = False
        self.db.close()        


###############################################################################
# shutdown ####################################################################
def shutdown_application ():
    """cleanup stuff"""
    Log("Stopping application")
    r.stop()
    Log("Application stopped")
    sys.exit(0)


###############################################################################
## main #######################################################################
if __name__ == "__main__":
    import argparse
    from Shutdown import Shutdown
    shutdown_application = Shutdown(shutdown_func=shutdown_application)

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--receiver", help="receive data", action="store_true")
    group.add_argument("--relais", help="relais data", action="store_true")
    args = parser.parse_args()

    if args.receiver:
        import mysql.connector as mc
        r = Receiver()
    if args.relais:
        r = Relais()

    r.run()

# eof #

