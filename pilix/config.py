# -*- coding: utf-8 -*-
###############################################################################
# Config.py                                                                   #
# (c) https://github.com/thomaspfeiffer-git 2017                              #
###############################################################################
"""lots of config stuff"""

import configparser as cfgparser
import os


CONFIGFILE = "pilix.ini"    
cfg = cfgparser.ConfigParser()

cfg.read(CONFIGFILE)

class CONFIG:
    class PIN:
         LED_Status  = int(cfg['Pilix']['pinLED_Status'])
         LED_Picture = int(cfg['Pilix']['pinLED_Picture'])

         BTN_Control = int(cfg['Pilix']['pinBTN_Control'])
         BTN_Battery = int(cfg['Pilix']['pinBTN_Battery'])

    class Camera:
         Intervall = int(cfg['Camera']['Intervall'])
         Width     = int(cfg['Camera']['Width'])
         Height    = int(cfg['Camera']['Height'])
         Quality   = int(cfg['Camera']['Quality'])

    class API:
         url = cfg['Pilix']['urlAPI']

    class File:
         csv = cfg['Pilix']['CSV']
         log = cfg['Pilix']['Logfile']
         picdir = cfg['Pilix']['PicDir']

    class APP:
         delayToShutdown = int(cfg['Pilix']['delayToShutdown'])

# eof #

