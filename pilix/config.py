# -*- coding: utf-8 -*-
###############################################################################
# Config.py                                                                   #
# (c) https://github.com/thomaspfeiffer-git 2017                              #
###############################################################################
"""lots of config stuff"""

import configparser as cfgparser
import os
import sys


CONFIGFILE = "pilix.ini"    
cfg = cfgparser.ConfigParser()
cfg.read(CONFIGFILE)

CREDENTIALS = os.path.expanduser('~') + "/credientials/pilix.cred"
cred = cfgparser.ConfigParser()
cred.read(CREDENTIALS)


class CONFIG:
    class PIN:
        LED_Status  = int(cfg['Pilix']['pinLED_Status'])
        LED_Picture = int(cfg['Pilix']['pinLED_Picture'])

        BTN_Control = int(cfg['Pilix']['pinBTN_Control'])

        BTN_Battery = int(cfg['Pilix']['pinBTN_Battery'])  # input
        BatteryControl = int(cfg['Pilix']['pinBatteryControl']) # output

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
        autostart = True if len(sys.argv) == 2 and sys.argv[1] == "autostart" else False

    class Livetracking:
        SECRET = cred['Livetracking']['SECRET']
        IP_ADDRESS_SERVER = cred['Livetracking']['IP_ADDRESS_SERVER']
        UDP_PORT = int(cred['Livetracking']['UDP_PORT'])
        MAX_PACKET_SIZE = int(cred['Livetracking']['MAX_PACKET_SIZE'])

# eof #

