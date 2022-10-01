# -*- coding: utf-8 -*-
###############################################################################
# Config.py                                                                   #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2019                   #
###############################################################################
"""
Configs for Sandpile.py.
"""

from datetime import datetime

###############################################################################
class CONFIG:
    class PILE:
        X = 500
        Y = 500
        MAX_GRAINS_PER_FIELD = 4
        GRAINS = X * Y

    class COLORS:
        BG_PILE = "Black"
        BG_TEXT = "Grey"
        GRAIN = { 0: "Black", 1: "Yellow", 2: "Orange", 3: "Red" }

    class COORDINATES:
        XPOS   = 100
        YPOS   = 100


###############################################################################
def filename (extension):
    return "sandpiles/sandpile_{}x{}_{}.{}".format(CONFIG.PILE.X,CONFIG.PILE.Y,
                                                   datetime.now().strftime("%Y%m%d_%H%M%S"),
                                                   extension)

# eof #

