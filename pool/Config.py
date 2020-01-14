# -*- coding: utf-8 -*-
###############################################################################
# Config.py                                                                   #
# (c) https://github.com/thomaspfeiffer-git 2019, 2020                        #
###############################################################################
"""lots of config stuff"""

import configparser as cfgparser

CONFIGFILE = "ventilation.ini"
cfg = cfgparser.ConfigParser()
cfg.read(CONFIGFILE)

class CONFIG:
    class Fans:
        fan_in1 = int(cfg['Fans']['fan_in1'])
        fan_in2 = int(cfg['Fans']['fan_in2'])
        fan_out = int(cfg['Fans']['fan_out'])
        fan_box = int(cfg['Fans']['fan_box'])

    class Buttons:
        btn_toggle = int(cfg['Buttons']['btn_toggle'])

    class Schedule:
        schedule = cfg['Schedule']['schedule']

# eof #

