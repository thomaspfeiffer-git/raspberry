#!/usr/bin/python3
# -*- coding: utf-8 -*-

import platform
import sys
sys.path.append('../libs')

from sensors.CPU import CPU

cpu = CPU()
print(cpu.read_temperature())

### eof ###

