#!/usr/bin/python
################################################################################
# clock.py                                                                     #
# Build an analog clock with LEDs.                                             #
# (c) https://github.com/thomaspfeiffer-git 2015                               #
################################################################################
"""clock.py: control of an analog clock built from 60 three color LEDs"""

import signal
from time import sleep, localtime, strftime
import sys
from threading import Lock
import traceback


from Lightness import Lightness
from SPI_const import SPI_const
from MCP23x17 import MCP23x17
from MCP23017 import MCP23017
from MCP23S17 import MCP23S17


PIN_PWM = 12 # BCM GPIO 18


tech     = 'tech'
tech_i2c = 'i2c'
tech_spi = 'spi'
device   = 'device'
bank     = 'bank'
bit      = 'bit'


# I2C (MCP23017) 
# Addresses of MCP23017 components
i2c_devices = (0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27)
i2c         = MCP23017(i2c_devices)

# SPI (MCP23S17) 
spi_lock    = Lock()
spi_devices = (0x00, 0x01, 0x02, 0x03)    # Addresses of MCP23S17 components
spi         = MCP23S17(SPI_const.CS1, spi_devices, spi_lock)


bits_red   = {0: {tech: i2c, device: 0x23, bank: "A", bit: "0b00000001"}, \
              1: {tech: i2c, device: 0x23, bank: "A", bit: "0b00001000"}, \
              2: {tech: i2c, device: 0x23, bank: "A", bit: "0b01000000"}, \
              3: {tech: i2c, device: 0x23, bank: "B", bit: "0b01000000"}, \
              4: {tech: i2c, device: 0x23, bank: "B", bit: "0b00001000"}, \
              5: {tech: i2c, device: 0x20, bank: "A", bit: "0b00000001"}, \
              6: {tech: i2c, device: 0x20, bank: "A", bit: "0b00001000"}, \
              7: {tech: i2c, device: 0x20, bank: "A", bit: "0b01000000"}, \
              8: {tech: i2c, device: 0x20, bank: "B", bit: "0b01000000"}, \
              9: {tech: i2c, device: 0x20, bank: "B", bit: "0b00001000"}, \
             10: {tech: i2c, device: 0x24, bank: "A", bit: "0b00000001"}, \
             11: {tech: i2c, device: 0x24, bank: "A", bit: "0b00001000"}, \
             12: {tech: i2c, device: 0x24, bank: "A", bit: "0b01000000"}, \
             13: {tech: i2c, device: 0x24, bank: "B", bit: "0b01000000"}, \
             14: {tech: i2c, device: 0x24, bank: "B", bit: "0b00001000"}, \
             15: {tech: i2c, device: 0x21, bank: "A", bit: "0b00000001"}, \
             16: {tech: i2c, device: 0x21, bank: "A", bit: "0b00001000"}, \
             17: {tech: i2c, device: 0x21, bank: "A", bit: "0b01000000"}, \
             18: {tech: i2c, device: 0x21, bank: "B", bit: "0b01000000"}, \
             19: {tech: i2c, device: 0x21, bank: "B", bit: "0b00001000"}, \
             20: {tech: i2c, device: 0x22, bank: "A", bit: "0b00000001"}, \
             21: {tech: i2c, device: 0x22, bank: "A", bit: "0b00001000"}, \
             22: {tech: i2c, device: 0x22, bank: "A", bit: "0b01000000"}, \
             23: {tech: i2c, device: 0x22, bank: "B", bit: "0b01000000"}, \
             24: {tech: i2c, device: 0x22, bank: "B", bit: "0b00001000"}, \
             25: {tech: i2c, device: 0x25, bank: "A", bit: "0b00000001"}, \
             26: {tech: i2c, device: 0x25, bank: "A", bit: "0b00001000"}, \
             27: {tech: i2c, device: 0x25, bank: "A", bit: "0b01000000"}, \
             28: {tech: i2c, device: 0x25, bank: "B", bit: "0b01000000"}, \
             29: {tech: i2c, device: 0x25, bank: "B", bit: "0b00001000"}, \
             30: {tech: i2c, device: 0x26, bank: "A", bit: "0b00000001"}, \
             31: {tech: i2c, device: 0x26, bank: "A", bit: "0b00001000"}, \
             32: {tech: i2c, device: 0x26, bank: "A", bit: "0b01000000"}, \
             33: {tech: i2c, device: 0x26, bank: "B", bit: "0b01000000"}, \
             34: {tech: i2c, device: 0x26, bank: "B", bit: "0b00001000"}, \
             35: {tech: i2c, device: 0x27, bank: "A", bit: "0b00000001"}, \
             36: {tech: i2c, device: 0x27, bank: "A", bit: "0b00001000"}, \
             37: {tech: i2c, device: 0x27, bank: "A", bit: "0b01000000"}, \
             38: {tech: i2c, device: 0x27, bank: "B", bit: "0b01000000"}, \
             39: {tech: i2c, device: 0x27, bank: "B", bit: "0b00001000"}, \
             40: {tech: spi, device: 0x01, bank: "A", bit: "0b00000001"}, \
             41: {tech: spi, device: 0x01, bank: "A", bit: "0b00001000"}, \
             42: {tech: spi, device: 0x01, bank: "A", bit: "0b01000000"}, \
             43: {tech: spi, device: 0x01, bank: "B", bit: "0b01000000"}, \
             44: {tech: spi, device: 0x01, bank: "B", bit: "0b00001000"}, \
             45: {tech: spi, device: 0x02, bank: "A", bit: "0b00000001"}, \
             46: {tech: spi, device: 0x02, bank: "A", bit: "0b00001000"}, \
             47: {tech: spi, device: 0x02, bank: "A", bit: "0b01000000"}, \
             48: {tech: spi, device: 0x02, bank: "B", bit: "0b01000000"}, \
             49: {tech: spi, device: 0x02, bank: "B", bit: "0b00001000"}, \
             50: {tech: spi, device: 0x03, bank: "A", bit: "0b00000001"}, \
             51: {tech: spi, device: 0x03, bank: "A", bit: "0b00001000"}, \
             52: {tech: spi, device: 0x03, bank: "A", bit: "0b01000000"}, \
             53: {tech: spi, device: 0x03, bank: "B", bit: "0b01000000"}, \
             54: {tech: spi, device: 0x03, bank: "B", bit: "0b00001000"}, \
             55: {tech: spi, device: 0x00, bank: "A", bit: "0b00000001"}, \
             56: {tech: spi, device: 0x00, bank: "A", bit: "0b00001000"}, \
             57: {tech: spi, device: 0x00, bank: "A", bit: "0b01000000"}, \
             58: {tech: spi, device: 0x00, bank: "B", bit: "0b01000000"}, \
             59: {tech: spi, device: 0x00, bank: "B", bit: "0b00001000"} }

bits_green = {0: {tech: i2c, device: 0x23, bank: "A", bit: "0b00000010"}, \
              1: {tech: i2c, device: 0x23, bank: "A", bit: "0b00010000"}, \
              2: {tech: i2c, device: 0x23, bank: "A", bit: "0b10000000"}, \
              3: {tech: i2c, device: 0x23, bank: "B", bit: "0b00100000"}, \
              4: {tech: i2c, device: 0x23, bank: "B", bit: "0b00000100"}, \
              5: {tech: i2c, device: 0x20, bank: "A", bit: "0b00000010"}, \
              6: {tech: i2c, device: 0x20, bank: "A", bit: "0b00010000"}, \
              7: {tech: i2c, device: 0x20, bank: "A", bit: "0b10000000"}, \
              8: {tech: i2c, device: 0x20, bank: "B", bit: "0b00100000"}, \
              9: {tech: i2c, device: 0x20, bank: "B", bit: "0b00000100"}, \
             10: {tech: i2c, device: 0x24, bank: "A", bit: "0b00000010"}, \
             11: {tech: i2c, device: 0x24, bank: "A", bit: "0b00010000"}, \
             12: {tech: i2c, device: 0x24, bank: "A", bit: "0b10000000"}, \
             13: {tech: i2c, device: 0x24, bank: "B", bit: "0b00100000"}, \
             14: {tech: i2c, device: 0x24, bank: "B", bit: "0b00000100"}, \
             15: {tech: i2c, device: 0x21, bank: "A", bit: "0b00000010"}, \
             16: {tech: i2c, device: 0x21, bank: "A", bit: "0b00010000"}, \
             17: {tech: i2c, device: 0x21, bank: "A", bit: "0b10000000"}, \
             18: {tech: i2c, device: 0x21, bank: "B", bit: "0b00100000"}, \
             19: {tech: i2c, device: 0x21, bank: "B", bit: "0b00000100"}, \
             20: {tech: i2c, device: 0x22, bank: "A", bit: "0b00000010"}, \
             21: {tech: i2c, device: 0x22, bank: "A", bit: "0b00010000"}, \
             22: {tech: i2c, device: 0x22, bank: "A", bit: "0b10000000"}, \
             23: {tech: i2c, device: 0x22, bank: "B", bit: "0b00100000"}, \
             24: {tech: i2c, device: 0x22, bank: "B", bit: "0b00000100"}, \
             25: {tech: i2c, device: 0x25, bank: "A", bit: "0b00000010"}, \
             26: {tech: i2c, device: 0x25, bank: "A", bit: "0b00010000"}, \
             27: {tech: i2c, device: 0x25, bank: "A", bit: "0b10000000"}, \
             28: {tech: i2c, device: 0x25, bank: "B", bit: "0b00100000"}, \
             29: {tech: i2c, device: 0x25, bank: "B", bit: "0b00000100"}, \
             30: {tech: i2c, device: 0x26, bank: "A", bit: "0b00000010"}, \
             31: {tech: i2c, device: 0x26, bank: "A", bit: "0b00010000"}, \
             32: {tech: i2c, device: 0x26, bank: "A", bit: "0b10000000"}, \
             33: {tech: i2c, device: 0x26, bank: "B", bit: "0b00100000"}, \
             34: {tech: i2c, device: 0x26, bank: "B", bit: "0b00000100"}, \
             35: {tech: i2c, device: 0x27, bank: "A", bit: "0b00000010"}, \
             36: {tech: i2c, device: 0x27, bank: "A", bit: "0b00010000"}, \
             37: {tech: i2c, device: 0x27, bank: "A", bit: "0b10000000"}, \
             38: {tech: i2c, device: 0x27, bank: "B", bit: "0b00100000"}, \
             39: {tech: i2c, device: 0x27, bank: "B", bit: "0b00000100"}, \
             40: {tech: spi, device: 0x01, bank: "A", bit: "0b00000010"}, \
             41: {tech: spi, device: 0x01, bank: "A", bit: "0b00010000"}, \
             42: {tech: spi, device: 0x01, bank: "A", bit: "0b10000000"}, \
             43: {tech: spi, device: 0x01, bank: "B", bit: "0b00100000"}, \
             44: {tech: spi, device: 0x01, bank: "B", bit: "0b00000100"}, \
             45: {tech: spi, device: 0x02, bank: "A", bit: "0b00000010"}, \
             46: {tech: spi, device: 0x02, bank: "A", bit: "0b00010000"}, \
             47: {tech: spi, device: 0x02, bank: "A", bit: "0b10000000"}, \
             48: {tech: spi, device: 0x02, bank: "B", bit: "0b00100000"}, \
             49: {tech: spi, device: 0x02, bank: "B", bit: "0b00000100"}, \
             50: {tech: spi, device: 0x03, bank: "A", bit: "0b00000010"}, \
             51: {tech: spi, device: 0x03, bank: "A", bit: "0b00010000"}, \
             52: {tech: spi, device: 0x03, bank: "A", bit: "0b10000000"}, \
             53: {tech: spi, device: 0x03, bank: "B", bit: "0b00100000"}, \
             54: {tech: spi, device: 0x03, bank: "B", bit: "0b00000100"}, \
             55: {tech: spi, device: 0x00, bank: "A", bit: "0b00000010"}, \
             56: {tech: spi, device: 0x00, bank: "A", bit: "0b00010000"}, \
             57: {tech: spi, device: 0x00, bank: "A", bit: "0b10000000"}, \
             58: {tech: spi, device: 0x00, bank: "B", bit: "0b00100000"}, \
             59: {tech: spi, device: 0x00, bank: "B", bit: "0b00000100"} }

bits_blue  = {0: {tech: i2c, device: 0x23, bank: "A", bit: "0b00000100"}, \
              1: {tech: i2c, device: 0x23, bank: "A", bit: "0b00100000"}, \
              2: {tech: i2c, device: 0x23, bank: "B", bit: "0b10000000"}, \
              3: {tech: i2c, device: 0x23, bank: "B", bit: "0b00010000"}, \
              4: {tech: i2c, device: 0x23, bank: "B", bit: "0b00000010"}, \
              5: {tech: i2c, device: 0x20, bank: "A", bit: "0b00000100"}, \
              6: {tech: i2c, device: 0x20, bank: "A", bit: "0b00100000"}, \
              7: {tech: i2c, device: 0x20, bank: "B", bit: "0b10000000"}, \
              8: {tech: i2c, device: 0x20, bank: "B", bit: "0b00010000"}, \
              9: {tech: i2c, device: 0x20, bank: "B", bit: "0b00000010"}, \
             10: {tech: i2c, device: 0x24, bank: "A", bit: "0b00000100"}, \
             11: {tech: i2c, device: 0x24, bank: "A", bit: "0b00100000"}, \
             12: {tech: i2c, device: 0x24, bank: "B", bit: "0b10000000"}, \
             13: {tech: i2c, device: 0x24, bank: "B", bit: "0b00010000"}, \
             14: {tech: i2c, device: 0x24, bank: "B", bit: "0b00000010"}, \
             15: {tech: i2c, device: 0x21, bank: "A", bit: "0b00000100"}, \
             16: {tech: i2c, device: 0x21, bank: "A", bit: "0b00100000"}, \
             17: {tech: i2c, device: 0x21, bank: "B", bit: "0b10000000"}, \
             18: {tech: i2c, device: 0x21, bank: "B", bit: "0b00010000"}, \
             19: {tech: i2c, device: 0x21, bank: "B", bit: "0b00000010"}, \
             20: {tech: i2c, device: 0x22, bank: "A", bit: "0b00000100"}, \
             21: {tech: i2c, device: 0x22, bank: "A", bit: "0b00100000"}, \
             22: {tech: i2c, device: 0x22, bank: "B", bit: "0b10000000"}, \
             23: {tech: i2c, device: 0x22, bank: "B", bit: "0b00010000"}, \
             24: {tech: i2c, device: 0x22, bank: "B", bit: "0b00000010"}, \
             25: {tech: i2c, device: 0x25, bank: "A", bit: "0b00000100"}, \
             26: {tech: i2c, device: 0x25, bank: "A", bit: "0b00100000"}, \
             27: {tech: i2c, device: 0x25, bank: "B", bit: "0b10000000"}, \
             28: {tech: i2c, device: 0x25, bank: "B", bit: "0b00010000"}, \
             29: {tech: i2c, device: 0x25, bank: "B", bit: "0b00000010"}, \
             30: {tech: i2c, device: 0x26, bank: "A", bit: "0b00000100"}, \
             31: {tech: i2c, device: 0x26, bank: "A", bit: "0b00100000"}, \
             32: {tech: i2c, device: 0x26, bank: "B", bit: "0b10000000"}, \
             33: {tech: i2c, device: 0x26, bank: "B", bit: "0b00010000"}, \
             34: {tech: i2c, device: 0x26, bank: "B", bit: "0b00000010"}, \
             35: {tech: i2c, device: 0x27, bank: "A", bit: "0b00000100"}, \
             36: {tech: i2c, device: 0x27, bank: "A", bit: "0b00100000"}, \
             37: {tech: i2c, device: 0x27, bank: "B", bit: "0b10000000"}, \
             38: {tech: i2c, device: 0x27, bank: "B", bit: "0b00010000"}, \
             39: {tech: i2c, device: 0x27, bank: "B", bit: "0b00000010"}, \
             40: {tech: spi, device: 0x01, bank: "A", bit: "0b00000100"}, \
             41: {tech: spi, device: 0x01, bank: "A", bit: "0b00100000"}, \
             42: {tech: spi, device: 0x01, bank: "B", bit: "0b10000000"}, \
             43: {tech: spi, device: 0x01, bank: "B", bit: "0b00010000"}, \
             44: {tech: spi, device: 0x01, bank: "B", bit: "0b00000010"}, \
             45: {tech: spi, device: 0x02, bank: "A", bit: "0b00000100"}, \
             46: {tech: spi, device: 0x02, bank: "A", bit: "0b00100000"}, \
             47: {tech: spi, device: 0x02, bank: "B", bit: "0b10000000"}, \
             48: {tech: spi, device: 0x02, bank: "B", bit: "0b00010000"}, \
             49: {tech: spi, device: 0x02, bank: "B", bit: "0b00000010"}, \
             50: {tech: spi, device: 0x03, bank: "A", bit: "0b00000100"}, \
             51: {tech: spi, device: 0x03, bank: "A", bit: "0b00100000"}, \
             52: {tech: spi, device: 0x03, bank: "B", bit: "0b10000000"}, \
             53: {tech: spi, device: 0x03, bank: "B", bit: "0b00010000"}, \
             54: {tech: spi, device: 0x03, bank: "B", bit: "0b00000010"}, \
             55: {tech: spi, device: 0x00, bank: "A", bit: "0b00000100"}, \
             56: {tech: spi, device: 0x00, bank: "A", bit: "0b00100000"}, \
             57: {tech: spi, device: 0x00, bank: "B", bit: "0b10000000"}, \
             58: {tech: spi, device: 0x00, bank: "B", bit: "0b00010000"}, \
             59: {tech: spi, device: 0x00, bank: "B", bit: "0b00000010"} }

bits = {}


###############################################################################
# InitBits ####################################################################
def InitBits(pattern):
    """initiates all bits (aka all ports for all LEDs) with pattern"""
    for d in i2c_devices:
        bits[i2c, d, "A"] = pattern
        bits[i2c, d, "B"] = pattern

    for d in spi_devices:
        bits[spi, d, "A"] = pattern
        bits[spi, d, "B"] = pattern


###############################################################################
# GetBank #####################################################################
def GetBank(string):
    """returns the register of the MCP23x17 for bank A or B respectively"""
    if (string == "A"):
        return MCP23x17.OLATA
    elif (string == "B"):
        return MCP23x17.OLATB
    else:
        print("Unknown bank!")
        # TODO: Exception!
        return MCP23x17.OLATA


###############################################################################
# WriteBits ###################################################################
def WriteBits():
    """writes all bits to the ports"""
    for k in bits:
        # print "Tech: ", k[0], "Device: ", k[1], "Bank: ", k[2], "Pattern: ", bits[k]
        k[0].send(k[1], GetBank(k[2]), bits[k])


###############################################################################
# AllOff ######################################################################
def AllOff():
    """set all ports to 0"""
    InitBits(0b00000000)
    WriteBits()


###############################################################################
# Cleanup #####################################################################
def Cleanup():
    """cleanup"""
    AllOff()


###############################################################################
# Exit ########################################################################
def Exit():
    """stuff to be done on exit"""
    Cleanup()
    spi.close()
   
    lightness.stop()
    lightness.join()
    # TODO: GPIO.cleanup()
    print("Exit")
    sys.exit()

def _Exit(__s, __f):
    """exit for signal handler"""
    print("_Exit")
    Exit()


###############################################################################
# Main ########################################################################
def Main():
    """main part"""
    bTest = True
    h = m = s = 0
    loopcounter = 0

    def adjust_hms(__h, __m, __s, __loopcounter):
        """deal with 'overflow' of hours, minutes, and seconds"""
        if (__h >= 60):
            __h = 0
            __loopcounter += 1

        if (__m >= 60):
            __m = 0
        if (__s >= 60):
            __s = 0

        if (__h < 0):
            __h = 59
            __loopcounter -= 1

        if (__m < 0):
            __m = 59
        if (__s < 0):
            __s = 59
        return (__h, __m, __s, __loopcounter)

    while(1):
        if (not bTest):
            hour, m, s = strftime("%H:%M:%S", localtime()).split(":")
            s = int(s)
            m = int(m)
            hour = int(hour)
            h = int((hour % 12) * 5) + int(m/12)
            # print "h (computed LED ID):", h, "m:", m, "s:", s, "hour:", hour
        else:
            (h, m, s, loopcounter) = adjust_hms(h+1, m+1, s+1, loopcounter)

        InitBits(0b00000000)

        if (not bTest):
            bits[bits_red[h][tech], bits_red[h][device], bits_red[h][bank]]        = int(bits_red[h][bit], 2)
            bits[bits_green[m][tech], bits_green[m][device], bits_green[m][bank]] |= int(bits_green[m][bit], 2)
            bits[bits_blue[s][tech], bits_blue[s][device], bits_blue[s][bank]]    |= int(bits_blue[s][bit], 2)
        
            if ((hour >= 7) and (hour < 20)): 
                # make seconds white ...
                bits[bits_red[s][tech], bits_red[s][device], bits_red[s][bank]]       |= int(bits_red[s][bit], 2)
                bits[bits_green[s][tech], bits_green[s][device], bits_green[s][bank]] |= int(bits_green[s][bit], 2)

                # ... and display constant hours (0/12, 1, 2, 3, 4, 5, ...)
                for hhh in range (0, 60, 5):
                    bits[bits_blue[hhh][tech], bits_blue[hhh][device], bits_blue[hhh][bank]] |= int(bits_blue[hhh][bit], 2)


        if (bTest):
            # All white; 20 lights on at once.
            bits[bits_red[h][tech], bits_red[h][device], bits_red[h][bank]]       = int(bits_red[h][bit], 2)
            bits[bits_green[h][tech], bits_green[h][device], bits_green[h][bank]] |= int(bits_green[h][bit], 2)
            bits[bits_blue[h][tech], bits_blue[h][device], bits_blue[h][bank]]    |= int(bits_blue[h][bit], 2)

            #if (loopcounter % 3 == 0):
            #    bits[bits_red[h][tech], bits_red[h][device], bits_red[h][bank]]       = int(bits_red[h][bit], 2)
            #if (loopcounter % 3 == 1):
            #    bits[bits_green[h][tech], bits_green[h][device], bits_green[h][bank]] = int(bits_green[h][bit], 2)
            #if (loopcounter % 3 == 2):
            #    bits[bits_blue[h][tech], bits_blue[h][device], bits_blue[h][bank]]    = int(bits_blue[h][bit], 2)

            j = h
            for _ in range (0, 20):
                bits[bits_red[j][tech], bits_red[j][device], bits_red[j][bank]]       |= int(bits_red[j][bit], 2)
                bits[bits_green[j][tech], bits_green[j][device], bits_green[j][bank]] |= int(bits_green[j][bit], 2)
                bits[bits_blue[j][tech], bits_blue[j][device], bits_blue[j][bank]]    |= int(bits_blue[j][bit], 2)

                #if (loopcounter % 3 == 0):
                #    bits[bits_red[j][tech], bits_red[j][device], bits_red[j][bank]]       |= int(bits_red[j][bit], 2)
                #if (loopcounter % 3 == 1):
                #    bits[bits_green[j][tech], bits_green[j][device], bits_green[j][bank]] |= int(bits_green[j][bit], 2)
                #if (loopcounter % 3 == 2):
                #    bits[bits_blue[j][tech], bits_blue[j][device], bits_blue[j][bank]]    |= int(bits_blue[j][bit], 2)

                j += 1
                if (j >= 60):
                    j = 0

        WriteBits()
        sleep(0.1)



###############################################################################
###############################################################################
signal.signal(signal.SIGTERM, _Exit)
lightness = Lightness(PIN_PWM, spi_lock)
lightness.start()

try:
    Main()

except KeyboardInterrupt:
    Exit()

except SystemExit:                  # Done in signal handler (method _Exit()) #
    pass

except:
    print(traceback.print_exc())

finally:        # All cleanup is done in KeyboardInterrupt or signal handler. #
    pass

### eof ###

