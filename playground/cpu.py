#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
sys.path.append('../libs/sensors')

from CPU import CPU

cpu = CPU()
print cpu.read()
