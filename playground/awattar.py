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
import json
from schedule import every, repeat, run_pending
import time
from urllib.request import urlopen




###############################################################################
###############################################################################
class Awattar (object):
    url = "https://api.awattar.at/v1/marketdata"

    def __init__ (self):
        self.data = { 'hourly ratings': None,
                      'lowest price': None }

    @repeat(every().hour.at(":01"))
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


###############################################################################
## main #######################################################################
if __name__ == "__main__":
    awattar = Awattar()
    awattar.update_data()

    import pprint
    pprint.pprint(awattar.data)

    """
    while True:
        run_pending()
        time.sleep(1)
    """

# eof #

