# -*- coding: utf-8 -*-
############################################################################
# pagination.py                                                            #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2017                #
############################################################################
"""provides the pagination logic for the WeatherApp:
   . on touch event switch to next screen
   . after a certain amount of time fall back to main screen
   . when indicated, first touch event will set brightness to max level
"""

import sys

sys.path.append('../libraries')
from touchevent import Touchevent

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
        return Touchevent.event()
 
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

