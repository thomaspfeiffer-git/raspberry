# -*- coding: utf-8 -*-
############################################################################
# touchevent.py                                                            #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2017                #
############################################################################
"""send the touch event to the brightness controller.
   if brightness was not at full level, the brightness
   controller sets brightness to full. in this case, False is retured.
   otherwise if the event shall be handled by the caller, True is returned.
"""

import json
import sys
from urllib.error import HTTPError, URLError 
from urllib.request import urlopen

sys.path.append('../../libs')
from Logging import Log

from config import CONFIG

class Touchevent (object):
    @staticmethod
    def event (event=None):
        """return True if the event shall be handled by the caller,
           otherwise False."""
        try:
            with urlopen(CONFIG.URL_BRIGHTNESS_CONTROL) as response:
                data = json.loads(response.read().decode("utf-8"))
        except (HTTPError, URLError):
            Log("Error: {0[0]} {0[1]}".format(sys.exc_info()))
        else:
            return data['FullBrightness']
        return True

# eof #

