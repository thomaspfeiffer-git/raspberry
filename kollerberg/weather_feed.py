#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# weather_feed.py                                                             #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2018                   #
###############################################################################
"""
Receives UDP data from our summer cottage and distributes it to the local
rrd database and to the sensor value queue.
"""

### usage ####
# nohup ./weather_feed.py 2>&1 > weather_feed.log &


import configparser as cfgparser
import rrdtool
import socket
import sys
import threading
import time

sys.path.append('../libs')

from Commons import Digest
from Logging import Log
from SensorQueue2 import SensorQueueClient_write
from SensorValue2 import SensorValue, SensorValue_Data
from Shutdown import Shutdown

CREDENTIALS = "/home/pi/configs/weather_feed.cred"
QUEUE_INI = "/home/pi/configs/weatherqueue.ini"
RRDFILE_WEATHER = "/schild/weather/weather_kollerberg.rrd"
RRDFILE_PARTICULATES = "/schild/weather/airparticulates.rrd"

pik_i = "pik_i"
pik_a = "pik_a"
pik_k = "pik_k"
PIs = [pik_i, pik_a, pik_k]

particulates_1 = "particulates_1"
particulates_2 = "particulates_2"
Particulates = [particulates_1, particulates_2]

data = { p: None for p in PIs+Particulates }


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
        data[source] = values
        # data['pik_k'] = "N:10.00:10.00:10.00:10.00:1013.25:0.00"
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
###############################################################################
class ToQueue (threading.Thread):
    def __init__ (self):
        threading.Thread.__init__(self)

        self.sq = SensorQueueClient_write(QUEUE_INI)
        self.qv_kb_i_t = SensorValue("ID_21", "Temp KB indoor", SensorValue_Data.Types.Temp, "°C")
        self.qv_kb_i_h = SensorValue("ID_22", "Humi KB indoor", SensorValue_Data.Types.Humi, "% rF")
        self.qv_kb_p   = SensorValue("ID_23", "Pressure KB",    SensorValue_Data.Types.Pressure, "hPa")

        self.qv_kb_a_t = SensorValue("ID_24", "Temp KB outdoor", SensorValue_Data.Types.Temp, "°C")
        self.qv_kb_a_h = SensorValue("ID_25", "Humi KB outdoor", SensorValue_Data.Types.Humi, "% rF")

        self.qv_kb_k_t = SensorValue("ID_26", "Temp KB basement", SensorValue_Data.Types.Temp, "°C")
        self.qv_kb_k_h = SensorValue("ID_27", "Humi KB basement", SensorValue_Data.Types.Humi, "% rF")

        self.sq.register(self.qv_kb_i_t)
        self.sq.register(self.qv_kb_i_h)
        self.sq.register(self.qv_kb_p)
        self.sq.register(self.qv_kb_a_t)
        self.sq.register(self.qv_kb_a_h)
        self.sq.register(self.qv_kb_k_t)
        self.sq.register(self.qv_kb_k_h)

        self._running = True

    def run (self):
        while self._running:
            if data[pik_i] is not None:
                self.qv_kb_i_t.value = "{:.1f}".format(float(data[pik_i].split(':')[1]))
                self.qv_kb_i_h.value = "{:.1f}".format(float(data[pik_i].split(':')[4]))
                self.qv_kb_p.value   = "{:.1f}".format(float(data[pik_i].split(':')[5]))
            if data[pik_a] is not None:
                self.qv_kb_a_t.value = "{:.1f}".format(float(data[pik_a].split(':')[1]))
                self.qv_kb_a_h.value = "{:.1f}".format(float(data[pik_a].split(':')[4]))
            if data[pik_k] is not None:
                self.qv_kb_k_t.value = "{:.1f}".format(float(data[pik_k].split(':')[1]))
                self.qv_kb_k_h.value = "{:.1f}".format(float(data[pik_k].split(':')[4]))

            for _ in range(600):  # interruptible sleep
                if not self._running:
                    break
                time.sleep(0.1)

    def stop (self):
        self._running = False


###############################################################################
# ToRRD #######################################################################
class ToRRD (threading.Thread):
    def __init__ (self):
        threading.Thread.__init__(self)

        self.DS_TEMP1 = "DS_TEMP1"
        self.DS_TEMP2 = "DS_TEMP2"
        self.DS_TCPU  = "DS_TCPU"
        self.DS_HUMI  = "DS_HUMI"
        self.DS_PRESS = "DS_PRESS"
        self.DS_AIRQ  = "DS_AIRQ"
        self.DS = { pik_i: { self.DS_TEMP1: 'kb_i_t1', 
                             self.DS_TEMP2: 'kb_i_t2',
                             self.DS_TCPU : 'kb_i_tcpu',
                             self.DS_HUMI : 'kb_i_humi',
                             self.DS_PRESS: 'kb_i_press',
                             self.DS_AIRQ:  'kb_i_airquality' },
                    pik_a: { self.DS_TEMP1: 'kb_a_t1',
                             self.DS_TEMP2: 'kb_a_t2',
                             self.DS_TCPU : 'kb_a_tcpu',
                             self.DS_HUMI : 'kb_a_humi',
                             self.DS_PRESS: 'kb_a_press',
                             self.DS_AIRQ:  'kb_a_airquality' },
                    pik_k: { self.DS_TEMP1: 'kb_k_t1',
                             self.DS_TEMP2: 'kb_k_t2',
                             self.DS_TCPU : 'kb_k_tcpu',
                             self.DS_HUMI : 'kb_k_humi',
                             self.DS_PRESS: 'kb_k_press', 
                             self.DS_AIRQ:  'kb_k_airquality' }
                  } 

        self._running = True

    @staticmethod
    def update_rrd (db, template, data):
        template = template.rstrip(":")
        data     = data.rstrip(":")
        # Log(template)
        # Log(data)
        try:
            rrdtool.update(db, "--template", template, data)
        except rrdtool.OperationalError:
            Log("Cannot update rrd database: {0[0]} {0[1]}".format(sys.exc_info()))

    def rrd_weather (self):
        data_complete = True
        rrd_template = ""
        rrd_data = "N:"

        for p in PIs:
            if not data[p]:
                data_complete = False
            else: 
                rrd_template += self.DS[p][self.DS_TEMP1] + ":" + \
                                self.DS[p][self.DS_TEMP2] + ":" + \
                                self.DS[p][self.DS_TCPU]  + ":" + \
                                self.DS[p][self.DS_HUMI]  + ":" + \
                                self.DS[p][self.DS_PRESS] + ":" + \
                                self.DS[p][self.DS_AIRQ] + ":"
                rrd_data += data[p].split("N:")[1].rstrip() + ":"

        if data_complete:
            self.update_rrd(RRDFILE_WEATHER, rrd_template, rrd_data)

    def rrd_particulates (self):
        data_complete = True
        rrd_template = ""
        rrd_data = "N:"
        for p in Particulates:
            if not data[p]:
                data_complete = False
            else:
                try:
                    rrd_template += data[p].split(":N:")[0] + ":"
                    rrd_data += data[p].split(":N:")[1] + ":"
                except IndexError:
                    Log("Wrong data format: {0[0]} {0[1]}".format(sys.exc_info()))
                    Log("data[p]: {}".format(data[p]))
                    return

        if data_complete:
            self.update_rrd(RRDFILE_PARTICULATES, rrd_template, rrd_data)

    def run (self):
        while self._running:
            self.rrd_weather()
            self.rrd_particulates()

            for _ in range(600):  # interruptible sleep
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
    to_rrd.stop()
    to_rrd.join()
    to_queue.stop()
    to_queue.join()
    udp.stop()
    udp.join()
    Log("Application stopped")
    sys.exit(0)


###############################################################################
# main ########################################################################
if __name__ == '__main__':
    shutdown_app = Shutdown(shutdown_func=shutdown_application)

    udp = UDP_Receiver()
    to_queue = ToQueue()
    to_rrd = ToRRD()

    udp.start()
    to_queue.start()
    to_rrd.start()

    while True:
        time.sleep(120)

# eof #

