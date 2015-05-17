#!/usr/bin/python
###############################################################################################
# clock.py                                                                                    #
# Build an analog clock with LEDs.                                                            #
# (c) https://github.com/thomaspfeiffer-git May 2015                                          #
###############################################################################################

import signal
from time import sleep, localtime, strftime
import sys
import traceback


from Lightness import Lightness
from SPI_const import SPI_const
from MCP23x17 import MCP23x17
from MCP23017 import MCP23017
from MCP23S17 import MCP23S17


tech     = 'tech'
tech_i2c = 'i2c'
tech_spi = 'spi'
device   = 'device'
bank     = 'bank'
bit      = 'bit'


# I2C (MCP23017)
i2c_devices = (0x20, 0x21, 0x22, 0x25)    # Addresses of MCP23017 components
i2c         = MCP23017(i2c_devices)

# SPI (MCP23S17) 
spi_devices = (0x00, 0x02)    # Addresses of MCP23S17 components
spi         = MCP23S17(SPI_const.CS1,spi_devices)


bits_red   = {0: {tech: i2c, device: 0x20, bank: "A", bit: "0b00000001"}, \
              1: {tech: i2c, device: 0x20, bank: "A", bit: "0b00001000"}, \
              2: {tech: i2c, device: 0x20, bank: "A", bit: "0b01000000"}, \
              3: {tech: i2c, device: 0x20, bank: "B", bit: "0b01000000"}, \
              4: {tech: i2c, device: 0x20, bank: "B", bit: "0b00001000"}, \
              5: {tech: i2c, device: 0x21, bank: "A", bit: "0b00000001"}, \
              6: {tech: i2c, device: 0x21, bank: "A", bit: "0b00001000"}, \
              7: {tech: i2c, device: 0x21, bank: "A", bit: "0b01000000"}, \
              8: {tech: i2c, device: 0x21, bank: "B", bit: "0b01000000"}, \
              9: {tech: i2c, device: 0x21, bank: "B", bit: "0b00001000"}, \
             10: {tech: i2c, device: 0x22, bank: "A", bit: "0b00000001"}, \
             11: {tech: i2c, device: 0x22, bank: "A", bit: "0b00001000"}, \
             12: {tech: i2c, device: 0x22, bank: "A", bit: "0b01000000"}, \
             13: {tech: i2c, device: 0x22, bank: "B", bit: "0b01000000"}, \
             14: {tech: i2c, device: 0x22, bank: "B", bit: "0b00001000"}, \
             15: {tech: i2c, device: 0x25, bank: "A", bit: "0b00000001"}, \
             16: {tech: i2c, device: 0x25, bank: "A", bit: "0b00001000"}, \
             17: {tech: i2c, device: 0x25, bank: "A", bit: "0b01000000"}, \
             18: {tech: i2c, device: 0x25, bank: "B", bit: "0b01000000"}, \
             19: {tech: i2c, device: 0x25, bank: "B", bit: "0b00001000"} }

bits_green = {0: {tech: i2c, device: 0x20, bank: "A", bit: "0b00000010"}, \
              1: {tech: i2c, device: 0x20, bank: "A", bit: "0b00010000"}, \
              2: {tech: i2c, device: 0x20, bank: "A", bit: "0b10000000"}, \
              3: {tech: i2c, device: 0x20, bank: "B", bit: "0b00100000"}, \
              4: {tech: i2c, device: 0x20, bank: "B", bit: "0b00000100"}, \
              5: {tech: i2c, device: 0x21, bank: "A", bit: "0b00000010"}, \
              6: {tech: i2c, device: 0x21, bank: "A", bit: "0b00010000"}, \
              7: {tech: i2c, device: 0x21, bank: "A", bit: "0b10000000"}, \
              8: {tech: i2c, device: 0x21, bank: "B", bit: "0b00100000"}, \
              9: {tech: i2c, device: 0x21, bank: "B", bit: "0b00000100"}, \
             10: {tech: i2c, device: 0x22, bank: "A", bit: "0b00000010"}, \
             11: {tech: i2c, device: 0x22, bank: "A", bit: "0b00010000"}, \
             12: {tech: i2c, device: 0x22, bank: "A", bit: "0b10000000"}, \
             13: {tech: i2c, device: 0x22, bank: "B", bit: "0b00100000"}, \
             14: {tech: i2c, device: 0x22, bank: "B", bit: "0b00000100"}, \
             15: {tech: i2c, device: 0x25, bank: "A", bit: "0b00000010"}, \
             16: {tech: i2c, device: 0x25, bank: "A", bit: "0b00010000"}, \
             17: {tech: i2c, device: 0x25, bank: "A", bit: "0b10000000"}, \
             18: {tech: i2c, device: 0x25, bank: "B", bit: "0b00100000"}, \
             19: {tech: i2c, device: 0x25, bank: "B", bit: "0b00000100"} }

bits_blue  = {0: {tech: i2c, device: 0x20, bank: "A", bit: "0b00000100"}, \
              1: {tech: i2c, device: 0x20, bank: "A", bit: "0b00100000"}, \
              2: {tech: i2c, device: 0x20, bank: "B", bit: "0b10000000"}, \
              3: {tech: i2c, device: 0x20, bank: "B", bit: "0b00010000"}, \
              4: {tech: i2c, device: 0x20, bank: "B", bit: "0b00000010"}, \
              5: {tech: i2c, device: 0x21, bank: "A", bit: "0b00000100"}, \
              6: {tech: i2c, device: 0x21, bank: "A", bit: "0b00100000"}, \
              7: {tech: i2c, device: 0x21, bank: "B", bit: "0b10000000"}, \
              8: {tech: i2c, device: 0x21, bank: "B", bit: "0b00010000"}, \
              9: {tech: i2c, device: 0x21, bank: "B", bit: "0b00000010"}, \
             10: {tech: i2c, device: 0x22, bank: "A", bit: "0b00000100"}, \
             11: {tech: i2c, device: 0x22, bank: "A", bit: "0b00100000"}, \
             12: {tech: i2c, device: 0x22, bank: "B", bit: "0b10000000"}, \
             13: {tech: i2c, device: 0x22, bank: "B", bit: "0b00010000"}, \
             14: {tech: i2c, device: 0x22, bank: "B", bit: "0b00000010"}, \
             15: {tech: i2c, device: 0x25, bank: "A", bit: "0b00000100"}, \
             16: {tech: i2c, device: 0x25, bank: "A", bit: "0b00100000"}, \
             17: {tech: i2c, device: 0x25, bank: "B", bit: "0b10000000"}, \
             18: {tech: i2c, device: 0x25, bank: "B", bit: "0b00010000"}, \
             19: {tech: i2c, device: 0x25, bank: "B", bit: "0b00000010"} }


bits = {}



###############################################################################
# InitBits ####################################################################
def InitBits(pattern):
   global bits

   for d in i2c_devices:
      bits[i2c,d,"A"] = pattern
      bits[i2c,d,"B"] = pattern

   for d in spi_devices:
      bits[spi,d,"A"] = pattern
      bits[spi,d,"B"] = pattern



###############################################################################
# GetBank #####################################################################
def GetBank(string):
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
  for k in bits:
     # print "Tech: ", k[0], "Device: ", k[1], "Bank: ", k[2], "Pattern: ", bits[k]
     k[0].send(k[1], GetBank(k[2]), bits[k])


###############################################################################
# AllOff ######################################################################
def AllOff():
   InitBits(0b00000000)
   WriteBits()



###############################################################################
# Cleanup #####################################################################
def Cleanup():
   AllOff()



###############################################################################
# Exit ########################################################################
def Exit():
   Cleanup()
   lightness.stop()
   lightness.join()
   # TODO: GPIO.cleanup()
   print("Exit")
   sys.exit()

def _Exit(s,f):
   print("_Exit")
   Exit()


###############################################################################
# Main ########################################################################
def Main():
   while(1):
      h, m, s = strftime("%H:%M:%S", localtime()).split(":")
      s = int(s) % 20
      m = int(m) % 20
      h = int(h) % 20
      # print s, clock_seconds[s][tech], clock_seconds[s][device], clock_seconds[s][bank], clock_seconds[s][bit]
      # print m, clock_minutes[m][tech], clock_minutes[m][device], clock_minutes[m][bank], clock_minutes[m][bit]
      # print h, clock_hours[h][tech], clock_hours[h][device], clock_hours[h][bank], clock_hours[h][bit]

      InitBits(0b00000000)
      bits[bits_red[h][tech], bits_red[h][device], bits_red[h][bank]]        = int(bits_red[h][bit],2)
      bits[bits_green[m][tech], bits_green[m][device], bits_green[m][bank]] |= int(bits_green[m][bit],2)
      bits[bits_blue[s][tech], bits_blue[s][device], bits_blue[s][bank]]    |= int(bits_blue[s][bit],2)
      WriteBits()
      sleep(1)



###############################################################################
###############################################################################
signal.signal(signal.SIGTERM, _Exit)
lightness = Lightness()
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


