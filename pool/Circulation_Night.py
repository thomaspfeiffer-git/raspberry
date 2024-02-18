#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# Circulation_Night.py                                                        #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2024                   #
###############################################################################

"""
Controls the circulation pump during night.
Saving energy according to https://api.awattar.at/v1/marketdata
"""

### Usage ###
# TODO


from datetime import datetime
import json
import sys
import threading
import time
from urllib.request import urlopen

sys.path.append("../libs/")
from Logging import Log
from Shutdown import Shutdown


###############################################################################
# Awattar #####################################################################
class Awattar (threading.Thread):
    url = "https://api.awattar.at/v1/marketdata"

    def __init__ (self):
        threading.Thread.__init__(self)
        self.data = { 'valid': False,
                      'lowest price': None }
        self._running = False

    def update_data (self):
        def empty_data ():
            return { 'start_timestamp': datetime.now(),
                     'end_timestamp': datetime.now(),
                     'marketprice': -99.99 }

        try:
            data = json.loads(urlopen(self.url).read())['data']
        except Exception as err:
            Log(f"Error while reading from {self.url}: {err}")
            data = [ empty_data() for _ in range(24) ]
            lowest_price = empty_data()
        else:
            lowest_price = data[0]
            for hour in data:
                hour['start_timestamp'] = datetime.fromtimestamp(int(hour['start_timestamp']/1000))
                hour['end_timestamp'] = datetime.fromtimestamp(int(hour['end_timestamp']/1000))
                hour['marketprice'] = hour['marketprice']

                Log(f"hour['start_timestamp'].hour: {hour['start_timestamp'].hour}")
                if hour['start_timestamp'].hour >= 10 and hour['start_timestamp'].hour <= 15:
                    if hour['marketprice'] < lowest_price['marketprice']:
                        lowest_price = hour

        Log(f"lowest_price: {lowest_price}")
        self.data['lowest price'] = lowest_price
        self.data['valid'] = True
        Log(f"Updated data from {self.url}")

    def run (self):
        self._running = True
        self.update_data()
        while self._running:
            if datetime.now().minute == 1:  # get new data once per hour
                self.update_data()
            for _ in range(500):    # interruptible sleep for 50 seconds
                time.sleep(0.1)
                if not self._running:
                    break

    def stop (self):
        self._running = False


###############################################################################
# Control #####################################################################
class Control (threading.Thread):
    def __init__ (self):
        threading.Thread.__init__(self)
        self._running = False

    def run (self):
        self._running = True
        while self._running:
            time.sleep(0.1)

    def stop (self):
        self._running = False


###############################################################################
# Shutdown stuff ##############################################################
def shutdown_application ():
    """cleanup stuff"""
    Log("Stopping application")
    control.stop()
    control.join()
    awattar.stop()
    awattar.join()
    Log("Application stopped")
    sys.exit(0)


###############################################################################
# main ########################################################################
if __name__ == "__main__":
    shutdown_application = Shutdown(shutdown_func=shutdown_application)

    awattar = Awattar()
    awattar.start()
    control = Control()
    control.start()

    while True:
        time.sleep(0.1)

# eof #

