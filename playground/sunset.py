#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
#                                                                             #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2020                   #
###############################################################################

from attrdict import AttrDict
from datetime import datetime, timezone, timedelta
import json
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

url = "https://api.sunrise-sunset.org/json?lat=48.2&lng=15.63333&formatted=0"

with urlopen(url) as response:
    data = AttrDict(json.loads(response.read().decode("utf-8")))
# TODO: exception handling


local_tz = datetime.now(timezone(timedelta(0))).astimezone().tzinfo
sunrise = datetime.strptime(data['results']['sunrise'], '%Y-%m-%dT%H:%M:%S%z').astimezone(local_tz)
sunset  = datetime.strptime(data['results']['sunset'],  '%Y-%m-%dT%H:%M:%S%z').astimezone(local_tz)

delta = timedelta(hours=1)
on = sunrise-delta <= datetime.now(tz=local_tz) <= sunset+delta

print(f"sunrise: {sunrise}")
print(f"sunset:  {sunset}")
print(f"on: {on}")

# eof #

