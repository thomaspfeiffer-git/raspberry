#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# awattar.py                                                                  #
# (c) https://github.com/thomaspfeiffer-git 2024                              #
###############################################################################

"""
Reads energy costs from awattar
https://www.awattar.at/services/api/
"""

from datetime import datetime
import json
import sys
from urllib.request import urlopen

sys.path.append("../libs/")
from Logging import Log

url = "https://api.awattar.at/v1/marketdata"

try:
    data = json.loads(urlopen(url).read())['data']
except Exception as err:
    Log(f"Error while reading from {url}: {err}")
else:
    for hour in data:
        hour['start_timestamp'] = datetime.fromtimestamp(int(hour['start_timestamp']/1000))
        hour['end_timestamp'] = datetime.fromtimestamp(int(hour['end_timestamp']/1000))
        hour['marketprice'] = hour['marketprice'] / 10.0
        hour['awattar price'] = ((hour['marketprice'] * 1.03) + 1.50) * 1.2
        hour['unit'] = "ct/kWh"

        print(f"{hour['start_timestamp']}: {hour['marketprice']:6.2f} {hour['unit']} (Awattar: {hour['awattar price']:6.2f} {hour['unit']})")

# eof #

