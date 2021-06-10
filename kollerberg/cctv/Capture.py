#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# Capture.py                                                                  #
# (c) https://github.com/thomaspfeiffer-git 2021                              #
###############################################################################
"""
"""

# === usage ===
# nohup ./Capture.py 2>&1 >capture.log &


# === you might need to install ===
# sudo pip3 install attrdict
# sudo pip3 install schedule


from attrdict import AttrDict
from datetime import datetime, timezone, timedelta
import json
import queue
import schedule
import shlex
import socket
import subprocess
import sys
import threading
import time
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

sys.path.append('../../libs')
from Shutdown import Shutdown
from Logging import Log


QSTOP = None

SCP_TIMEOUT = 120
SCP_BANDWIDTHFILE = "./scp_bandwidth"
TEMPDIR = "/ramdisk/"
DESTHOST = "seti-05"
DESTDIR = "/ramdisk/"


###############################################################################
# run_command #################################################################
def run_command(command: str):
    command = shlex.split(command)
    process = subprocess.Popen(command)
    process.wait()
    process.communicate()


###############################################################################
# bandwidth ###################################################################
def bandwidth():
    last_bw = None

    def read():
        nonlocal last_bw
        with open(SCP_BANDWIDTHFILE) as f:
            bw = f.readline().strip()
        if last_bw != bw:
            last_bw = bw
            Log(f"scp bandwidth set to {bw} Kbit/s")
        return bw
    return read


###############################################################################
# Daylight ####################################################################
class Daylight(object):
    def __init__(self):
        self.url = "https://api.sunrise-sunset.org/json?lat=48.2&lng=15.63333&formatted=0"
        self.__daylight = False
        self.last_daylight = None
        self.sunrise = None
        self.sunset = None
        self.local_tz = datetime.now(timezone(timedelta(0))).astimezone().tzinfo
        self.update_data()
        schedule.every().day.at("00:30").do(self.update_data)
        schedule.every().day.at("04:30").do(self.update_data)

    def __call__(self):
        self.calculate()
        return self.__daylight

    def update_data(self):
        try:
            with urlopen(self.url) as response:
                data = AttrDict(json.loads(response.read().decode("utf-8")))
        except (HTTPError, URLError, ConnectionResetError):
            Log("Error: {0[0]} {0[1]}".format(sys.exc_info()))
        except socket.timeout:
            Log("socket.timeout: {0[0]} {0[1]}".format(sys.exc_info()))
        else:
            t_format = '%Y-%m-%dT%H:%M:%S%z'
            self.sunrise = datetime.strptime(data['results']['sunrise'], t_format).astimezone(self.local_tz)
            self.sunset = datetime.strptime(data['results']['sunset'], t_format).astimezone(self.local_tz)
            Log(f"Sunrise: {self.sunrise}")
            Log(f"Sunset: {self.sunset}")

    def calculate(self):
        delta = timedelta(hours=1)
        self.__daylight = self.sunrise-delta <= datetime.now(tz=self.local_tz) <= self.sunset+delta
        if self.__daylight != self.last_daylight:
            Log(f"Daylight: {self.__daylight}")
            self.last_daylight = self.__daylight

    def scheduler(self):
        schedule.run_pending()


###############################################################################
# TakePictures ################################################################
class TakePictures(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.raspistill = 'raspistill -ae 64,0xff,0x808000 -a 4 -a "Kollerberg %Y-%m-%d %X - {:05d}" -o {}'

    def run(self):
        self._running = True

        i = 0
        while self._running:
            if daylight():
                filename = f"{TEMPDIR}pic_{datetime.now().strftime('%Y%m%d-%H%M%S')}_{i:05d}.jpg"
                run_command(self.raspistill.format(i, filename))
                Log(f"{filename} captured")
                self.queue.put(filename)
                i += 1
            else:
                i = 0   # Reset counter during the night
                time.sleep(0.5)

        # Log("Sending QSTOP")
        self.queue.put(QSTOP)

    def stop(self):
        self._running = False


###############################################################################
# Deliver #####################################################################
class Deliver(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.scp = f"timeout -k 10 -v {SCP_TIMEOUT} scp -l {{}} -q {{}} {DESTHOST}:{DESTDIR}"

    def run(self):
        self._running = True

        while self._running:
            filename = self.queue.get()
            self.queue.task_done()
            if filename == QSTOP:
                Log(f"Got '{filename}' from queue")
                self._running = False
            else:
                run_command(self.scp.format(bandwidth(), filename))
                run_command(f"rm -f {filename}")
                Log(f"{filename} delivered")

    def stop(self):
        self._running = False


###############################################################################
# shutdown_application ########################################################
def shutdown_application():
    """called on shutdown; stops all threads"""
    Log("Stopping application.")
    pictures.stop()
    pictures.join()
    deliver.join()         # stopping itself due to QSTOP
    Log("Application stopped.")
    sys.exit(0)


###############################################################################
# Main ########################################################################
if __name__ == '__main__':
    shutdown = Shutdown(shutdown_func=shutdown_application)
    bandwidth = bandwidth()
    queue_ = queue.Queue(maxsize=2)

    daylight = Daylight()

    pictures = TakePictures(queue_)
    pictures.start()

    deliver = Deliver(queue_)
    deliver.start()

    while True:
        daylight.scheduler()
        time.sleep(1)

# eof #
