#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# awattar.py                                                                  #
# (c) https://github.com/thomaspfeiffer-git 2024, 2025                        #
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
        awattar_net = ((hour['marketprice'] + abs(hour['marketprice']) * 0.03) + 1.50)
        hour['awattar price'] = awattar_net if awattar_net < 0.0 else awattar_net * 1.20
        hour['unit'] = "ct/kWh"

        print(f"{hour['start_timestamp']}: {hour['marketprice']:6.2f} {hour['unit']} (Awattar: {hour['awattar price']:6.2f} {hour['unit']})")

# eof #

