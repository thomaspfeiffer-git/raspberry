# -*- coding: utf-8 -*-
###############################################################################
# Config.py                                                                   #
# (c) https://github.com/thomaspfeiffer-git 2017                              #
###############################################################################
"""lots of config stuff"""

# configparser was named ConfigParser in Python 2.x
try:
    import configparser as cfgparser
except Exception:
    import ConfigParser as cfgparser 

import os


CONFIGFILE = "pilix.ini"    
cfg = cfgparser.ConfigParser()

cfg.read(CONFIGFILE)

class CONFIG:
    class PIN:
         # LED_Status  = int(cfg['Pilix']['pinLED_Status'])
         # LED_Picture = int(cfg['Pilix']['pinLED_Picture'])
         LED_Status  = int(cfg.get('Pilix', 'pinLED_Status'))
         LED_Picture = int(cfg.get('Pilix', 'pinLED_Picture'))

         # BTN_Control = int(cfg['Pilix']['pinBTN_Control'])
         # BTN_Battery = int(cfg['Pilix']['pinBTN_Battery'])
         BTN_Control = int(cfg.get('Pilix', 'pinBTN_Control'))
         BTN_Battery = int(cfg.get('Pilix', 'pinBTN_Battery'))

    class Camera:
         # Intervall = int(cfg['Camera']['Intervall'])
         Intervall = int(cfg.get('Camera', 'Intervall'))

    class API:
         # url = cfg['Pilix']['urlAPI']
         url = cfg.get('Pilix', 'urlAPI')

    class File:
         # csv = cfg['Pilix']['CSV']
         # log = cfg['Pilix']['Logfile']
         csv = cfg.get('Pilix', 'CSV')
         log = cfg.get('Pilix', 'Logfile')

    class APP:
         # delayToShutdown = int(cfg['Pilix']['delayToShutdown'])
         delayToShutdown = int(cfg.get('Pilix', 'delayToShutdown'))

# eof #

