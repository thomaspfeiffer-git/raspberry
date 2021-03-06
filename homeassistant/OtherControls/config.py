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
        BUTTON_ANTEROOM = "yellow2"
        BUTTON_RADIO = "SeaGreen1"

    class COORDINATES:
        WIDTH  = int(cfg['OtherControls']['width'])
        HEIGHT = int(cfg['OtherControls']['height'])
        XPOS   = int(cfg['OtherControls']['xpos'])
        YPOS   = int(cfg['OtherControls']['ypos'])

    class RADIO:
        BASE_URL = cfg['Radio']['base_url']


    CLICK_SOUND = "../sounds/click.mp3"

    URL_ANTEROOM_CONTROL   = "http://nano03:5000/toggle"
    URL_BRIGHTNESS_CONTROL = cfg['Brightness']['URL']

# eof #

