# -*- coding: utf-8 -*-
###############################################################################
# Config.py                                                                   #
# (c) https://github.com/thomaspfeiffer-git 2023                              #
###############################################################################
"""
config stuff
"""

import configparser

CONFIGFILE = "../config.ini"
cfg = configparser.ConfigParser()
cfg.read(CONFIGFILE)

class CONFIG:
    class APPLICATION:
        PORT = int(cfg['Awattar']['port'])

# eof #

