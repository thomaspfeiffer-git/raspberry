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


from datetime import datetime
from flask import Flask, jsonify, request
import json
import sys
import threading
import time
from urllib.request import urlopen

sys.path.append("../../libs/")
from Logging import Log
from SensorQueue2 import SensorQueueClient_write
from SensorValue2 import SensorValue, SensorValue_Data
from Shutdown import Shutdown

app = Flask(__name__)


###############################################################################
## Awattar ####################################################################
class Awattar (threading.Thread):
    url = "https://api.awattar.at/v1/marketdata"

    def __init__ (self):
        threading.Thread.__init__(self)
        self.data = { 'valid': False,
                      'hourly ratings': None,
                      'lowest price': None }

    def update_data (self):
        data = json.loads(urlopen(self.url).read())['data']
        lowest_price = data[0]
        for hour in data:
            hour['start_timestamp'] = datetime.fromtimestamp(int(hour['start_timestamp']/1000))
            hour['end_timestamp'] = datetime.fromtimestamp(int(hour['end_timestamp']/1000))
            hour['marketprice'] = ((hour['marketprice'] / 10.0 * 1.03) + 1.50)  * 1.2
            hour['unit'] = "ct/kWh"

            if hour['marketprice'] < lowest_price['marketprice']:
                lowest_price = hour

        self.data['hourly ratings'] = data
        self.data['lowest price'] = lowest_price
        self.data['valid'] = True
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
## Queue ######################################################################
class Queue (threading.Thread):
    def __init__ (self):
        threading.Thread.__init__(self)

        self.qv_price = SensorValue("ID_AW_01", "AWPrice", SensorValue_Data.Types.Aw_Price, "")
        self.qv_price_act = SensorValue("ID_AW_02", "AWPriceAct", SensorValue_Data.Types.Aw_Price, "ct/kWh")
        self.qv_price_next = SensorValue("ID_AW_03", "AWPriceNext", SensorValue_Data.Types.Aw_Price, "ct/kWh")
        self.qv_price_actnext = SensorValue("ID_AW_04", "AWPriceActNext", SensorValue_Data.Types.Aw_Price, "")
        self.qv_price_lowest = SensorValue("ID_AW_05", "AWPriceLowest", SensorValue_Data.Types.Aw_Price, "")

        self.sq = SensorQueueClient_write("../../../configs/weatherqueue.ini")
        self.sq.register(self.qv_price)
        self.sq.register(self.qv_price_act)
        self.sq.register(self.qv_price_next)
        self.sq.register(self.qv_price_actnext)
        self.sq.register(self.qv_price_lowest)

    def run (self):
        self._running = True

        while self._running:
            if awattar.data['valid']:
                price_act = f"{awattar.data['hourly ratings'][0]['marketprice']:.2f}"
                price_next = f"{awattar.data['hourly ratings'][1]['marketprice']:.2f}"
                price_actnext = f"{price_act} / {price_next}"
                price_lowest = f"{awattar.data['lowest price']['start_timestamp'].hour}:" + \
                               f"{awattar.data['lowest price']['start_timestamp'].minute:02d}: " + \
                               f"{awattar.data['lowest price']['marketprice']:.2f}"
                price = f"{price_act} / {price_next}\n{price_lowest}"
                # Log(f"price: {price}")
                self.qv_price.value = price
                self.qv_price_act.value = price_act
                self.qv_price_next.value = price_next
                self.qv_price_actnext.value = price_actnext
                self.qv_price_lowest.value = price_lowest

            for _ in range(600):    # interruptible sleep for 60 seconds
                time.sleep(0.1)
                if not self._running:
                    break

    def stop (self):
        self._running = False


###############################################################################
## Flask stuff ################################################################
@app.route('/awattar')
def API_Data ():
    Log("Data requested.")
    return jsonify(awattar.data)


###############################################################################
## Shutdown stuff #############################################################
def shutdown_application ():
    """cleanup stuff"""
    Log("Stopping application")
    queue.stop()
    queue.join()
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

    queue = Queue()
    queue.start()

    app.run(host="0.0.0.0", port=5002)

# eof #

