#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# awattar.py                                                                  #
# (c) https://github.com/thomaspfeiffer-git 2023                              #
###############################################################################

"""
Reads energy costs from awattar
https://www.awattar.at/services/api/
"""


"""
sudo pip3 install schedule

"""

from datetime import datetime
from flask import Flask, jsonify, request
import json
import sys
import threading
import time
from urllib.request import urlopen

sys.path.append("../../libs/")
from Logging import Log
from Shutdown import Shutdown

app = Flask(__name__)


###############################################################################
## Awattar ####################################################################
class Awattar (threading.Thread):
    url = "https://api.awattar.at/v1/marketdata"

    def __init__ (self):
        threading.Thread.__init__(self)
        self.data = { 'hourly ratings': None,
                      'lowest price': None }

    def update_data (self):
        data = json.loads(urlopen(self.url).read())['data']
        lowest_price = data[0]
        for hour in data:
            hour['start_timestamp'] = datetime.fromtimestamp(int(hour['start_timestamp']/1000))
            hour['end_timestamp'] = datetime.fromtimestamp(int(hour['end_timestamp']/1000))
            hour['marketprice'] /= 10.0
            hour['unit'] = "ct/kWh"

            if hour['marketprice'] < lowest_price['marketprice']:
                lowest_price = hour

        self.data['hourly ratings'] = data
        self.data['lowest price'] = lowest_price
        Log(f"Updated data from {self.url}")

    def run (self):
        self._running = True
        self.update_data()
        while self._running:
            if datetime.now().minute == 1:
                self.update_data()
            for _ in range(500):    # interruptible sleep for 50 seconds
                time.sleep(0.1)
                if not self._running:
                    break

    def stop (self):
        self._running = False


###############################################################################
# Flask stuff #################################################################
@app.route('/awattar')
def API_Data ():
    Log("Data requested.")
    return jsonify(awattar.data)


###############################################################################
## Shutdown stuff #############################################################
def shutdown_application ():
    """cleanup stuff"""
    Log("Stopping application")
    awattar.stop()
    awattar.join()
    Log("Application stopped")
    sys.exit(0)


###############################################################################
## main #######################################################################
if __name__ == "__main__":
    shutdown_application = Shutdown(shutdown_func=shutdown_application)

    awattar = Awattar()
    awattar.start()

    app.run(host="0.0.0.0", port=5002)

# eof #

