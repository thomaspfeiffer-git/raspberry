#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
#                                                                             #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2017                   #
###############################################################################

from attrdict import AttrDict
from datetime import datetime, timezone, timedelta
import json
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

url = "https://api.sunrise-sunset.org/json?lat=48.2&lng=15.63333&formatted=0"

with urlopen(url) as response:
    data = AttrDict(json.loads(response.read().decode("utf-8")))


sunrise = datetime.strptime(data['results']['sunrise'], '%Y-%m-%dT%H:%M:%S%z')
sunset  = datetime.strptime(data['results']['sunset'],  '%Y-%m-%dT%H:%M:%S%z')

print(f"sunrise: {sunrise}")
print(f"sunset:  {sunset}")


LOCAL_TIMEZONE = datetime.now(timezone(timedelta(0))).astimezone().tzinfo
print(LOCAL_TIMEZONE)

sunrise = sunrise.astimezone(LOCAL_TIMEZONE)
sunset  = sunset.astimezone(LOCAL_TIMEZONE)

print(f"sunrise: {sunrise}")
print(f"sunset:  {sunset}")

# eof #

