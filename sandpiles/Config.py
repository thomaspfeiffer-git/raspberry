###############################################################################
###############################################################################
"""
"""

class CONFIG:
    class PILE:
        X = 500
        Y = 500
        MAX_GRAINS_PER_FIELD = 4
        GRAINS = X * Y * (MAX_GRAINS_PER_FIELD-1)

    class COLORS:
        BG_PILE = "Black"
        BG_TEXT = "Grey"
        GRAIN = { 0: "Black", 1: "Yellow", 2: "Orange", 3: "Red" }

    class COORDINATES:
        XPOS   = 100
        YPOS   = 100

# eof #

