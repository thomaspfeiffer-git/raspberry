# -*- coding: utf-8 -*-
###############################################################################
# Config.py                                                                   #
# (c) https://github.com/thomaspfeiffer-git 2017                              #
###############################################################################
"""lots of config stuff"""

import configparser as cfgparser
import sys

CONFIGFILE = "pilix.ini"
cfg = cfgparser.ConfigParser()
cfg.read(CONFIGFILE)

CREDENTIALS = "/home/pi/credentials/pilix.cred"
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
        Interval_UDP_OnBattery = int(cfg['Livetracking']['Interval_UDP_OnBattery'])
        Interval_UDP_OnPowersupply = int(cfg['Livetracking']['Interval_UDP_OnPowersupply'])
        MaxHeight_UDP = int(cfg['Livetracking']['MaxHeight_UDP'])
        Interval_LoRa_OnBattery = int(cfg['Livetracking']['Interval_LoRa_OnBattery'])
        Interval_LoRa_OnPowersupply = int(cfg['Livetracking']['Interval_LoRa_OnPowersupply'])
        LoRa_Frequency=int(cfg['Livetracking']['LoRa_Frequency'])
        LoRa_TX_Power=cfg['Livetracking']['LoRa_TX_Power']
        LoRa_pinInterrupt=int(cfg['Livetracking']['LoRa_pinInterrupt'])
        LoRa_pinReset=int(cfg['Livetracking']['LoRa_pinReset'])
        SQL_USER = cred['Livetracking']['SQL_USER']
        SQL_PASSWORD = cred['Livetracking']['SQL_PASSWORD']

# eof #

