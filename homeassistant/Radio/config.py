# -*- coding: utf-8 -*-
###############################################################################
# Config.py                                                                   #
# (c) https://github.com/thomaspfeiffer-git 2017, 2021                        #
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
        BACKGROUND = "LightSkyBlue"
        FONT = "Black"
        BUTTON = "DodgerBlue"
        BUTTON_OFF = "Red"

    class COORDINATES:
        WIDTH  = int(cfg['Radio']['width'])
        HEIGHT = int(cfg['Radio']['height'])
        XPOS   = int(cfg['Radio']['xpos'])
        YPOS   = int(cfg['Radio']['ypos'])

    class APPLICATION:
        PORT   = int(cfg['Radio']['port'])

    URL_BRIGHTNESS_CONTROL = cfg['Brightness']['URL']

# eof #
