# -*- coding: utf-8 -*-
###############################################################################
# Config.py                                                                   #
# (c) https://github.com/thomaspfeiffer-git 2019                              #
###############################################################################
"""lots of config stuff"""

import configparser as cfgparser
import sys

CONFIGFILE = "ventilation.ini"
cfg = cfgparser.ConfigParser()
cfg.read(CONFIGFILE)

class CONFIG:
    class Fans:
        fan_in  = int(cfg['Fans']['fan_in'])
        fan_out = int(cfg['Fans']['fan_out'])
        fan_box = int(cfg['Fans']['fan_box'])

    class Buttons:
        btn_toggle = int(cfg['Buttons']['btn_toggle'])

# eof #

