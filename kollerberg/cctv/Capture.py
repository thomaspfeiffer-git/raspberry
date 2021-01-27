#!/usr/bin/python3
# -*- coding: utf-8 -*-
###############################################################################
# Capture.py                                                                  #
# (c) https://github.com/thomaspfeiffer-git 2021                              #
###############################################################################
"""
"""

### usage ###
# TODO

# TODO


from attrdict import AttrDict
from datetime import datetime, timezone, timedelta
import json
import queue
import threading
import socket
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.request import urlopen


sys.path.append('../../libs')
from Shutdown import Shutdown
from Logging import Log


QSTOP = None


###############################################################################
# Daylight ####################################################################
class Daylight(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.url = "https://api.sunrise-sunset.org/json?lat=48.2&lng=15.63333&formatted=0"
        self.__daylight = False

    @property
    def daylight(self):
        return self.__daylight

    def calculate(self):
        try:
            with urlopen(self.url) as response:
                data = AttrDict(json.loads(response.read().decode("utf-8")))
        except (HTTPError, URLError, ConnectionResetError):
            Log("Error: {0[0]} {0[1]}".format(sys.exc_info()))
        except socket.timeout:
            Log("socket.timeout: {0[0]} {0[1]}".format(sys.exc_info()))

        local_tz = datetime.now(timezone(timedelta(0))).astimezone().tzinfo
        sunrise = datetime.strptime(data['results']['sunrise'], '%Y-%m-%dT%H:%M:%S%z').astimezone(local_tz)
        sunset = datetime.strptime(data['results']['sunset'], '%Y-%m-%dT%H:%M:%S%z').astimezone(local_tz)

        delta = timedelta(hours=1)
        self.__daylight = sunrise-delta <= datetime.now(tz=local_tz) <= sunset+delta
        Log(f"daylight: {self.daylight}")

    def run(self):
        self._running = True
        while self._running:
            self.calculate()
            for _ in range(6000):    # interrruptible sleep for 10 minutes
                if not self._running:
                    break
                time.sleep(0.1)

    def stop(self):
        self._running = False


###############################################################################
# TakePictures ################################################################
class TakePictures(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        self._running = True

        i = 0
        while self._running:
            if daylight.daylight:
                # TODO: call raspistill
                Log(f"Putting '{i}' to queue")
                self.queue.put(i)
                i += 1
            else:
                time.sleep(0.5)

        Log("Sending QSTOP")
        self.queue.put(QSTOP)
        Log(f"'{self.__class__.__name__}' stopped")

    def stop(self):
        Log(f"Stopping '{self.__class__.__name__}'")
        self._running = False


###############################################################################
# Deliver #####################################################################
class Deliver(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        self._running = True

        while self._running:
            item = self.queue.get()
            Log(f"Got '{item}' from queue")
            self.queue.task_done()
            if item == QSTOP:
                self._running = False
            else:
                time.sleep(1)
                # TODO call scp
        Log(f"'{self.__class__.__name__}' stopped")

    def stop(self):
        Log(f"Stopping '{self.__class__.__name__}'")
        self._running = False


###############################################################################
# shutdown_application ########################################################
def shutdown_application():
    """called on shutdown; stops all threads"""
    Log("Stopping application.")
    pictures.stop()
    pictures.join()
    deliver.join()         # stopping itself due to QSTOP
    daylight.stop()
    daylight.join()
    Log("Application stopped.")
    sys.exit(0)


###############################################################################
# Main ########################################################################
if __name__ == '__main__':
    shutdown = Shutdown(shutdown_func=shutdown_application)
    queue_ = queue.Queue(maxsize=3)

    daylight = Daylight()
    daylight.start()

    pictures = TakePictures(queue_)
    pictures.start()

    deliver = Deliver(queue_)
    deliver.start()

    while True:
        time.sleep(0.5)

# eof #
