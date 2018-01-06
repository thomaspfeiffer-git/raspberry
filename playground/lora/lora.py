#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# lora.py                                                                     #
# Demo for sending and receiving data with the RFM96W LoRa module.            #
# Sourcecode taken and modified from:                                         #
# * https://github.com/ladecadence/pyRF95                                     #
# * https://github.com/PiInTheSky/lora-gateway/blob/master/gateway.c          #
# (c) https://github.com/thomaspfeiffer-git 2018                              #
###############################################################################
"""Demo for sending and receiving data with the RFM96W LoRa module."""

# Useful links:
# * Data sheet: http://www.hoperf.com/upload/rf/RFM95_96_97_98W.pdf
# * Adafruit: https://learn.adafruit.com/adafruit-rfm69hcw-and-rfm96-rfm95-rfm98-lora-packet-padio-breakouts
# Hints on distance tuning:
# http://wiki.dragino.com/index.php?title=LoRa_Questions#Check_the_Modem_Setting_in_Software


import argparse
import RPi.GPIO as GPIO
import spidev
import sys
import time

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

sys.path.append('.')
sys.path.append('../../libs')
from Logging import Log
from Shutdown import Shutdown
from actuators.SSD1306 import SSD1306

from actuators.RFM9x import RFM9x
from actuators.RFM9x_constants import *



LoRa_Cfg_Medium = { LR_Cfg_Reg1: BW_125KHZ | CODING_RATE_4_5,
                    LR_Cfg_Reg2: SPREADING_FACTOR_128CPS | RX_PAYLOAD_CRC_ON,
                    LR_Cfg_Reg3: MOBILE_NODE_MOBILE | AGC_AUTO_ON,
                    LR_Cfg_BW:   125.0 }

LoRa_Cfg_Telemetry = { LR_Cfg_Reg1: BW_41K7HZ | CODING_RATE_4_8,
                       LR_Cfg_Reg2: SPREADING_FACTOR_4096CPS | RX_PAYLOAD_CRC_ON,
                       LR_Cfg_Reg3: MOBILE_NODE_MOBILE | AGC_AUTO_ON,
                       LR_Cfg_BW:   41.7 }

LoRa_Cfg_Telemetry_Stable = { LR_Cfg_Reg1: BW_62K5HZ | CODING_RATE_4_8,
                              LR_Cfg_Reg2: SPREADING_FACTOR_4096CPS | RX_PAYLOAD_CRC_ON,
                              LR_Cfg_Reg3: MOBILE_NODE_MOBILE | AGC_AUTO_ON,
                              LR_Cfg_BW:   62.5 }


# LoRa_Cfg = LoRa_Cfg_Medium
LoRa_Cfg = LoRa_Cfg_Telemetry
# LoRa_Cfg = LoRa_Cfg_Telemetry_Stable

tx_interval = 15
frequency = 433500000
tx_power = 13



###############################################################################
# Exit ########################################################################
def shutdown_application ():
    """cleanup stuff"""
    rf95.set_mode_idle()
    rf95.cleanup()

    if disp:
        disp.clear()
        disp.display()

    sys.exit(0)


###############################################################################
###############################################################################
def Sender ():
    rf95.set_tx_power(tx_power)
    msg = ["finster war's, der Mond schien helle, als ein Wagen blitzeschnelle langsam um die runde Ecke fuhr.", "kurz"]

    count = 0
    while True:
        payload = "ID: {}@{} {}".format(count, time.strftime("%H%M%S"), msg[count % 2])
        Log("Sending Data \"{}\"".format(payload))
        rf95.send(rf95.str_to_data(payload))
        rf95.wait_packet_sent()
        Log("Data sent!\n")
        count += 1
        time.sleep(tx_interval);


###############################################################################
# Receiver ####################################################################
def Receiver ():
    global disp

    rf95.spi_write(REG_0C_LNA, LNA_BOOST_MAX) # TODO: find a better place for this
    # taken from https://github.com/PiInTheSky/lora-gateway/blob/master/gateway.c#L118

    disp = SSD1306()
    disp.begin()
    disp.clear()
    disp.display()

    xpos = 4
    ypos = 4
    width = disp.width
    height = disp.height
    image = Image.new('1', (width, height))
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    (_, textheight) = draw.textsize("Text", font=font)

    while True:
        while not rf95.available():
            pass

        draw.rectangle((0,0,width,height), outline=0, fill=255)
        y = ypos
        draw.text((xpos, y), "Zeit: {}".format(time.strftime("%X")), font=font, fill=0)

        data = rf95.recv()
        Log("RSSI: {}".format(rf95.last_rssi))

        str = "".join(map(chr, data))
        Log("{}\n".format(str))

        y += textheight
        draw.text((xpos, y), "RSSI: {}".format(rf95.last_rssi))
        y += textheight
        draw.text((xpos, y), "{}".format(str[:20]))

        disp.image(image)
        disp.display()


###############################################################################
# MyParser #################################################################### 
class MyParser(argparse.ArgumentParser):
    def error(self, message):
        """override error() in order to get a proper cleanup"""
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        shutdown_application()


###############################################################################
# Main ########################################################################
if __name__ == "__main__":
    shutdown = Shutdown(shutdown_func=shutdown_application)

    disp = None

    rf95 = RFM9x(config=LoRa_Cfg, frequency=frequency, int_pin=31, reset_pin=32) 
    if not rf95.init():
        Log("Error: RFM9x not found")
        rf95.cleanup()
        sys.exit(1)
    else:
        Log("RFM9x LoRa mode ok")

    parser = MyParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-r", "--receive", help="receive data", action="store_true")
    group.add_argument("-s", "--send", help="send data", action="store_true")
    args = parser.parse_args()
    if args.receive:
        Receiver()
    if args.send:
        Sender()

# eof #

