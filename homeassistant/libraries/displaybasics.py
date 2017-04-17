# -*- coding: utf-8 -*-
###############################################################################
# displaybasics.py                                                            #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2017                   #
###############################################################################
"""
"""


import tkinter as tk
import tkinter.ttk as ttk

from config import CONFIG


###############################################################################
# Basic display elements ######################################################
class Displayelement_Mixin (object):
    """provides the basic logic for calculating the grid pos of an element"""
    @property
    def gridpos (self):
        return self.__gridpos

    @gridpos.setter
    def gridpos (self, gridpos):
        self.__gridpos = gridpos


class Text (tk.Label, Displayelement_Mixin):
    """prints text"""
    """update of data is done in stringvar (must be of type tk.StringVar)"""
    def __init__ (self, frame, gridpos, text, stringvar, anchor, sticky, font, color):
        # TODO: type safety: stringvar
        super().__init__(frame, text=text, textvariable=stringvar, 
                         # justify="left", anchor=anchor, font=font,
                         justify="center", anchor=anchor, font=font,
                         foreground=color, background=CONFIG.COLORS.BACKGROUND)
        self.gridpos = gridpos+1 
        self.grid(row=gridpos, column=0, sticky=sticky)


class Image (tk.Label, Displayelement_Mixin):
    def __init__ (self, frame, gridpos, image):
        # TODO: type safety: image
        super().__init__(frame, image=image, background=CONFIG.COLORS.BACKGROUND)
        self.gridpos = gridpos+1 
        self.grid(row=gridpos, column=0, sticky="we")


class WeatherItem (Text):
    """draws a single weather item"""
    def __init__ (self, frame, gridpos, stringvar, font=None, color=None):
        super().__init__(frame, gridpos=gridpos, text=None, stringvar=stringvar, 
                         anchor="w", sticky="w", font=font, color=color)


class DateItem (Text):
    """draws a date line"""
    def __init__ (self, frame, gridpos, stringvar, font, color):
        super().__init__(frame, gridpos=gridpos, text=None, stringvar=stringvar, 
                         anchor="center", sticky="we", font=font, color=color)


class SeparatorText (Text):
    """prints separator text"""
    def __init__ (self, frame, gridpos, text=None, vartext=None, font=None):
        super().__init__(frame, gridpos=gridpos, text=text, stringvar=vartext,
                         anchor="w", sticky="we", font=font, color=CONFIG.COLORS.SEP)


class SeparatorLine (ttk.Separator, Displayelement_Mixin):
    """prints separator line"""
    def __init__ (self, frame, gridpos):
        super().__init__(frame, orient="horizontal")
        self.gridpos = gridpos+1
        self.grid(row=gridpos, column=0, sticky="we")


class Separator (Displayelement_Mixin): 
    """prints a separator which consists of a line and some text"""
    def __init__ (self, frame, gridpos, text=None, vartext=None, font=None):
        self.gridpos = SeparatorLine(frame=frame, gridpos=gridpos).gridpos
        if text is not None or vartext is not None:
            self.gridpos = SeparatorText(frame=frame, gridpos=self.gridpos,
                                         text=text, vartext=vartext, 
                                         font=font).gridpos

# eof #

