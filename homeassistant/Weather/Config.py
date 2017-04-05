# -*- coding: utf-8 -*-
###############################################################################
# Config.py                                                                   #
# (c) https://github.com/thomaspfeiffer-git 2016, 2017                        #
###############################################################################
"""lots of config stuff
   1) display properties
   2) fonts
   3) colors
   4) files
   5) misc stuff
"""

import configparser
import os

class CONFIG:
    """various config stuff"""
    CONFIGFILE = "../config.ini"    

    class FONTS:
        """definitions of fonts and font sizes"""
        FAMILY = "Helvetica"

        SIZE_NORMAL   = int(32)
        SIZE_FORECAST = int(SIZE_NORMAL / 2.0)
        SIZE_SMALL    = int(SIZE_NORMAL / 2.4)
        SIZE_TINY     = int(SIZE_NORMAL / 3.4)

    class COLORS:
        """definitions of colors"""
        BACKGROUND = "Moccasin"
        DATE       = "black"
        DESC       = "black"
        SEP        = "black"
        INDOOR     = "red"
        OUTDOOR    = "blue"
        FORECAST   = "SlateGrey"
        KIDSROOM   = "DeepSkyBlue"
        COTTAGE    = "ForestGreen"
        MISC       = "Indigo"
        WARDROBE   = "Gold"

    class IMAGES:
        """definitions of images and path to images"""
        PATH          = '../Resources'
        PIC_KIDSROOM  = os.path.join(PATH, 'child.png')
        PIC_COTTAGE   = os.path.join(PATH, 'cottage.png')

        ICON_SUNNY    = os.path.join(PATH, 'ico_sunny.png')
        ICON_CLOUDY   = os.path.join(PATH, 'ico_cloudy.png')
        ICON_OVERCAST = os.path.join(PATH, 'ico_overcast.png')
        ICON_RAINY    = os.path.join(PATH, 'ico_rainy.png')


    TIMETOFALLBACK = 15000 # Wait 15 seconds until fallback to main screen

    __cfg = configparser.ConfigParser()
    __cfg.read(CONFIGFILE)
    URL_BRIGHTNESS_CONTROL = __cfg['Brightness']['URL']

# eof #

