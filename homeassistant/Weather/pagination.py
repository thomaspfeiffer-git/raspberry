# -*- coding: utf-8 -*-
############################################################################
# pagination.py                                                            #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2017                #
############################################################################
"""
"""

import json
import sys
from urllib.error import HTTPError, URLError 
from urllib.request import urlopen

sys.path.append('../../libs')
from Logging import Log

from config import CONFIG


class Pagination (object):
    """pagination of screens with fallback to first (main) screen after
       CONFIG.TIMETOFALLBACK milliseconds
       triggered by bind("<Button-1>")"""
    def __init__ (self, master, screens, screennames):
        self.master  = master
        self.screens = screens
        self.screennames = screennames
        self.screenid = 0
        self.reset    = None
     
    def turn_page (self):
        """send the touch event to the brightness controller.
           if brightness was not at full level, the brightness
           controller sets brightness to full. in this case, no
           pagination shall be done."""
        try:
            with urlopen(CONFIG.URL_BRIGHTNESS_CONTROL) as response:
                data = json.loads(response.read().decode("utf-8"))
        except (HTTPError, URLError):
            Log("Error: {0[0]} {0[1]}".format(sys.exc_info()))
        else:
            return data['FullBrightness']
        return True
 
    def first_screen (self):
        """switch back to first screen after 
           CONFIG.TIMETOFALLBACK milliseconds"""
        if self.screenid != 0:
            self.screens[self.screennames[self.screenid]].grid_remove()
            self.screenid = 0
            self.screens[self.screennames[self.screenid]].grid()
        self.reset = None

    def next_screen (self, event):
        """do pagination of screens and set callback to first_screen()
           after CONFIG.TIMETOFALLBACK milliseconds"""

        if not self.turn_page():
            return

        if self.reset is not None:
            self.master.after_cancel(self.reset)
            self.reset = None

        self.screens[self.screennames[self.screenid]].grid_remove()
        self.screenid += 1
        if self.screenid >= len(self.screennames): 
            self.screenid = 0
        self.screens[self.screennames[self.screenid]].grid()

        self.reset = self.master.after(CONFIG.TIMETOFALLBACK, self.first_screen)

# eof #

