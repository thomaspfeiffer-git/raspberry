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
"""

import os

class CONFIG:
    """various config stuff"""

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
        KIDSROOM   = (0, 0xCC, 0xFF)
        COTTAGE    = (0x08, 0x8A, 0x08)
        MISC       = (0x08, 0x8A, 0x08)
        WARDROBE   = (0xFF, 0xCC, 0x00)

    class IMAGES:
        """definitions of images and path to images"""
        PATH          = 'data'
        PIC_KIDSROOM  = os.path.join(PATH, 'child.png')
        PIC_COTTAGE   = os.path.join(PATH, 'cottage.png')

        ICON_SUNNY    = os.path.join(PATH, 'ico_sunny.png')
        ICON_CLOUDY   = os.path.join(PATH, 'ico_cloudy.png')
        ICON_OVERCAST = os.path.join(PATH, 'ico_overcast.png')
        ICON_RAINY    = os.path.join(PATH, 'ico_rainy.png')


    TIMETOFALLBACK = 15 # Wait 15 seconds until fallback to main screen

# eof #

