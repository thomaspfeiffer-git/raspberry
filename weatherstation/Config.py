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
    WIDTH          = 320 # Screen resolution
    HEIGHT         = 480

    FONTSIZE       = int(HEIGHT / 8)
    FONTSIZE_SMALL = int(FONTSIZE / 2.4)
    FONTSIZE_TINY  = int(FONTSIZE / 3.4)

    MARGIN         = 3                 # Margin (pixels) from border
    SEP_Y          = int(FONTSIZE / 5) # Pixels between different elements

    class COLORS:
        """definitions of colors"""
        BACKGROUND = (255, 255, 255)
        DATE       = (0, 0, 0)
        DESC       = (0, 0, 0)
        SEP        = (0, 0, 0)
        INDOOR     = (255, 0, 0)
        OUTDOOR    = (0, 0, 255)
        KIDSROOM   = (0, 0xCC, 0xFF)
        MISC       = (0x08, 0x8A, 0x08)

    class IMAGES:
        """definitions of images and path to images"""
        PATH          = 'data'
        PIC_KIDSROOM  = os.path.join(PATH, 'child.png')
        PIC_TURTLE    = os.path.join(PATH, 'turtle.png')

        ICON_SUNNY    = os.path.join(PATH, 'ico_sunny.png')
        ICON_CLOUDY   = os.path.join(PATH, 'ico_cloudy.png')
        ICON_OVERCAST = os.path.join(PATH, 'ico_overcast.png')
        ICON_RAINY    = os.path.join(PATH, 'ico_rainy.png')

    TIMETOFALLBACK = 10 # Wait 10 seconds until fallback to main screen

# eof #

