#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# modbus_sdm630.py                                                            #
# (c) https://github.com/thomaspfeiffer-git 2023                              #
###############################################################################

"""
prototyping usage of SDM630 via modbus
"""


"""
# software

sudo pip3 install -U minimalmodbus

"""

import minimalmodbus

instrument = minimalmodbus.Instrument('/dev/ttyUSB1', 1)





# eof #

