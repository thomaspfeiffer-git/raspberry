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


url = "https://api.awattar.at/v1/marketdata"


@repeat(every().hour.at(":01"))
def update_data():
    data = json.loads(urlopen(url).read())['data']
    lowest_price = data[0]
    for hour in data:
        hour['start_timestamp'] = datetime.fromtimestamp(int(hour['start_timestamp']/1000))
        hour['end_timestamp'] = datetime.fromtimestamp(int(hour['end_timestamp']/1000))
        hour['marketprice'] /= 10.0
        hour['unit'] = "ct/kWh"

        if hour['marketprice'] < lowest_price['marketprice']:
            lowest_price = hour

    print(data)
    print(f"lowest price: {lowest_price}")


update_data()

"""
while True:
    run_pending()
    time.sleep(1)
"""
# eof #

