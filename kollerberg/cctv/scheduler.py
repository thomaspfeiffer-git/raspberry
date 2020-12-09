#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# scheduler.py                                                                #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2020                   #
###############################################################################

from attrdict import AttrDict
from datetime import datetime, timezone, timedelta
import json
import sys
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

sys.path.append("../../libs/")
from Logging import Log

url = "https://api.sunrise-sunset.org/json?lat=48.2&lng=15.63333&formatted=0"

if len(sys.argv) == 2:
    defaultvalue = int(str(sys.argv)[1])
else:
    defaultvalue = 1

try:
    with urlopen(url) as response:
        data = AttrDict(json.loads(response.read().decode("utf-8")))
except (HTTPError, URLError, ConnectionResetError):
    Log("Error: {0[0]} {0[1]}".format(sys.exc_info()))
    sys.exit(defaultvalue)
except socket.timeout:
    Log("socket.timeout: {0[0]} {0[1]}".format(sys.exc_info()))
    sys.exit(defaultvalue)

local_tz = datetime.now(timezone(timedelta(0))).astimezone().tzinfo
sunrise = datetime.strptime(data['results']['sunrise'], '%Y-%m-%dT%H:%M:%S%z').astimezone(local_tz)
sunset  = datetime.strptime(data['results']['sunset'],  '%Y-%m-%dT%H:%M:%S%z').astimezone(local_tz)

delta = timedelta(hours=1)
on = sunrise-delta <= datetime.now(tz=local_tz) <= sunset+delta

sys.exit(1 if on else 0)

# eof #

