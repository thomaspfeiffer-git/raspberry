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


### Packages you might need to install ###
# sudo pip3 install schedule


from datetime import datetime
import json
import schedule
import sys
import threading
import time
from urllib.request import urlopen

sys.path.append("../libs/")
from Logging import Log
from Shutdown import Shutdown


###############################################################################
# Awattar #####################################################################
class Awattar (object):
    url = "https://api.awattar.at/v1/marketdata"

    def __init__ (self):
        self.data = { 'valid': False,
                      'lowest_price': self.empty_data() }

    @staticmethod
    def empty_data ():
        return { 'start_timestamp': None,
                 'end_timestamp': None,
                 'marketprice': 999.99 }

    def update_data (self):
        lowest_price = self.empty_data()
        try:
            data = json.loads(urlopen(self.url).read())['data']
        except Exception as err:
            Log(f"Error while reading from {self.url}: {err}")
        else:
            for hour in data:
                hour['start_timestamp'] = datetime.fromtimestamp(int(hour['start_timestamp']/1000))
                hour['end_timestamp'] = datetime.fromtimestamp(int(hour['end_timestamp']/1000))
                hour['marketprice'] = hour['marketprice'] / 10.0

                # Activate pump only for some hours after midnight.
                if 0 <= hour['start_timestamp'].hour <= 5:
                    if hour['marketprice'] < lowest_price['marketprice']:
                        lowest_price = hour

        Log(f"Updated data from {self.url}.")
        if lowest_price['start_timestamp']:
            self.data['lowest_price'] = lowest_price
            self.data['valid'] = True
            Log(f"Lowest price at {self.cheapest_hour}:00: {self.data['lowest_price']['marketprice']:.2f} ct/kWh.")
        else:
            Log("Data not available yet.")

    @property
    def cheapest_hour (self):
        if self.data['valid']:
            return self.data['lowest_price']['start_timestamp'].hour
        else:
            return None


###############################################################################
# Control #####################################################################
class Control (threading.Thread):
    url_on = "http://localhost/on"
    url_off = "http://localhost/off"

    def __init__ (self):
        threading.Thread.__init__(self)
        self.pump_on = False
        self._running = False

    def on (self):
        if not self.pump_on:
            Log("Pump on")
            try:
                urlopen(self.url_on).read()
            except Exception as err:
                Log(f"Error opening url {self.url_on}: {err}")
                Log("Pump on failed.")
            else:
                self.pump_on = True

    def off (self):
        if self.pump_on:
            Log("Pump off")
            try:
                urlopen(self.url_off).read()
            except Exception as err:
                Log(f"Error opening url {self.url_off}: {err}")
                Log("Pump off failed.")
            else:
                self.pump_on = False

    def run (self):
        self._running = True
        while self._running:
            if awattar.data['valid']:
                # Log(f"cheapest hour: {awattar.cheapest_hour}")
                # if 23 == awattar.cheapest_hour:
                if datetime.now().hour == awattar.cheapest_hour:
                    self.on()
                else:
                    self.off()

            for _ in range(500):   # interruptible sleep for 50 seconds
                time.sleep(0.1)
                if not self._running:
                    break

        self.off()   # Cleanup

    def stop (self):
        self._running = False


###############################################################################
# Shutdown stuff ##############################################################
def shutdown_application ():
    """cleanup stuff"""
    Log("Stopping application")
    control.stop()
    control.join()
    Log("Application stopped")
    sys.exit(0)


###############################################################################
# main ########################################################################
if __name__ == "__main__":
    shutdown_application = Shutdown(shutdown_func=shutdown_application)

    awattar = Awattar()
    awattar.update_data()
    control = Control()
    control.start()

    schedule.every().day.at("23:15").do(awattar.update_data)
    schedule.every().day.at("14:15").do(awattar.update_data)

    while True:
        schedule.run_pending()
        time.sleep(1)

# eof #

