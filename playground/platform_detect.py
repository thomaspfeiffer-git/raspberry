#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# platform_detect.py                                                          #
# (c) https://github.com/thomaspfeiffer-git 2024                              #
###############################################################################
"""
"""


####
# sudo pip3 install --break-system-packages Adafruit-PlatformDetect

from adafruit_platformdetect import Detector
detector = Detector()
print("Chip id: ", detector.chip.id)
print("Board id: ", detector.board.id)

# Check for specific board models:
print("Pi 3B+? ", detector.board.RASPBERRY_PI_3B_PLUS)
print("BBB? ", detector.board.BEAGLEBONE_BLACK)
print("Orange Pi PC? ", detector.board.ORANGE_PI_PC)
print("generic Linux PC? ", detector.board.GENERIC_LINUX_PC)

# eof #

