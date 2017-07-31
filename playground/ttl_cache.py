#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
#############################################################################
# ttl_cache.py                                                              #
# (c) https://github.com/thomaspfeiffer-git 2017                            #
#############################################################################
"""demo programm for a ttl cache"""


# Usage: 
# nohup ./ttl_cache.py &


from attrdict import AttrDict
import cachetools.func
import json
import sys
from urllib.error import HTTPError, URLError 
from urllib.request import urlopen


sys.path.append('../libs')
from Logging import Log


@cachetools.func.ttl_cache(maxsize=16, ttl=60)
def ReadJsonURL_cached (url):
    try:
        with urlopen(url, timeout=15) as response:
            data = AttrDict(json.loads(response.read().decode("utf-8"))[1])
    except (HTTPError, URLError):
        Log("HTTPError, URLError: {0[0]} {0[1]}".format(sys.exc_info()))
    except socket.timeout: 
        Log("socket.timeout: {0[0]} {0[1]}".format(sys.exc_info())) 
    else:
        pass

# eof #

