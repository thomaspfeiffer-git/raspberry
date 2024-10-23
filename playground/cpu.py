#!/usr/bin/python3
# -*- coding: utf-8 -*-


####
# sudo pip3 install --break-system-packages Adafruit-PlatformDetect

from adafruit_platformdetect import Detector
import sys
sys.path.append('../libs')

from sensors.CPU import CPU

detector = Detector()
print(f"Board: {detector.board.id}")

cpu = CPU()
print(cpu.read_temperature())

### eof ###

