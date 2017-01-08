#!/usr/bin/python3
# -*- coding: utf-8 -*-
#############################################################################
# wardrobe.py                                                               #
# (c) https://github.com/thomaspfeiffer-git 2017                            #
#############################################################################
"""controls lighting of my wardrobe"""



# sensor id | gpio-in | gpio-out | usage |
# #1        | pin 15  | pin 16   | main area
# #2        | pin 31  | pin 32   | top drawer
# #3        | pin 35  | pin 36   | bottom drawer (opt.)
# #4        | pin 37  | pin 38   | top area (opt.)




# Lib: libs/pwm.py
# pin 12

# turtle/Reedcontact.py as example
# attention: has some logic for debouncing which causes a delay of 10 s
# until an opened door is recognized

# debouncing:
# https://www.raspberrypi.org/forums/viewtopic.php?t=137484&p=913137
# http://raspberrypihobbyist.blogspot.co.at/2014/11/debouncing-gpio-input.html






