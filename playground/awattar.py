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
import json
from urllib.request import urlopen


url = "https://api.awattar.at/v1/marketdata"
data_json = json.loads(urlopen(url).read())

for hour in range(3):
    timestamp = datetime.fromtimestamp(int(data_json['data'][hour]['start_timestamp']/1000))
    value = data_json['data'][hour]['marketprice'] / 10.0
    print(f"Timestamp: {timestamp}; Value: {value:.2f}")

# eof #

