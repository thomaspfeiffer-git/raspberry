###############################################################################
# Adafruit_GPIO_Platform.py                                                   #
# File fully refactored in 2024.                                              #
# TODO: rename file                                                           #
# (c) https://github.com/thomaspfeiffer-git 2024                              #
###############################################################################

from adafruit_platformdetect import Detector

# Platform identification constants.
UNKNOWN      = 0
RASPBERRY_PI = 1
NANOPI       = 2
MINNOWBOARD  = 3
NANOPC_T3    = 4


def platform_detect():
    detector = Detector()

    if "RASPBERRY" in detector.board.id:
        return RASPBERRY_PI
    elif "NANOPI" in detector.board.id:
        return NANOPI
    else:
        return UNKNOWN

# eof #

