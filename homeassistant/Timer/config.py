# -*- coding: utf-8 -*-
###############################################################################
# Config.py                                                                   #
# (c) https://github.com/thomaspfeiffer-git 2017                              #
###############################################################################
"""lots of config stuff
   1) display properties
   2) fonts
   3) colors
   4) files
   5) coordinates
   6) misc stuff
"""

import configparser
import os


CONFIGFILE = "../config.ini"    
cfg = configparser.ConfigParser()
cfg.read(CONFIGFILE)


class CONFIG:
    """various config stuff"""

    class FONTS:
        """definitions of fonts and font sizes"""
        FAMILY = "Arial"
        SIZE_NORMAL = int(20)

    class COLORS:
        """definitions of colors"""
        BACKGROUND = "Moccasin"
        BUTTON     = "DodgerBlue"

    class ALARM:
        """definitions of alarm stuff"""
        COLORS = ["red", "yellow", "blue"]
        DELAY  = 100   # milliseconds
        COUNT  = 150
        SOUND  = "kikeriki.mp3"

    class COORDINATES:
        WIDTH  = int(cfg['Timer']['width'])
        HEIGHT = int(cfg['Timer']['height'])
        XPOS   = int(cfg['Timer']['xpos'])
        YPOS   = int(cfg['Timer']['ypos'])

    CLICK_SOUND = "click.mp3"
    URL_BRIGHTNESS_CONTROL = cfg['Brightness']['URL']

# eof #

