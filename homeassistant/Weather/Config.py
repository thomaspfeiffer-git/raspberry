# -*- coding: utf-8 -*-
###############################################################################
# Screens.py                                                                  #
# (c) https://github.com/thomaspfeiffer-git 2016                              #
###############################################################################
"""lots of config stuff
   1) display properties
   2) colors
   3) files
"""
 
import os

class CONFIG:
    """various config stuff"""
    FONT              = "Helvetica"

    FONTSIZE          = int(32)
    FONTSIZE_FORECAST = int(FONTSIZE / 2.0)
    FONTSIZE_SMALL    = int(FONTSIZE / 2.4)
    FONTSIZE_TINY     = int(FONTSIZE / 3.4)

    class COLORS:
        """definitions of colors"""
        BACKGROUND = "white"
        DATE       = (0, 0, 0)
        DESC       = (0, 0, 0)
        SEP        = (0, 0, 0)
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

    TIMETOFALLBACK = 15 # Wait 10 seconds until fallback to main screen

# eof #

