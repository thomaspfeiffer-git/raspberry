#!/usr/bin/python

import smbus
import spidev
from time import sleep, localtime, strftime
import sys
import traceback

tech     = 'tech'
tech_i2c = 'i2c'
tech_spi = 'spi'
device   = 'device'
bank     = 'bank'
bit      = 'bit'


clock_seconds = {0: {tech: tech_i2c, device: 0x20, bank: "A", bit: "0b10000000"}, \
                 3: {tech: tech_i2c, device: 0x20, bank: "A", bit: "0b01000000"}, \
                 2: {tech: tech_i2c, device: 0x20, bank: "B", bit: "0b00000001"}, \
                 1: {tech: tech_i2c, device: 0x20, bank: "B", bit: "0b00000010"}, \
                 5: {tech: tech_i2c, device: 0x21, bank: "A", bit: "0b10000000"}, \
                 4: {tech: tech_i2c, device: 0x21, bank: "B", bit: "0b00000001"}, \
                 6: {tech: tech_i2c, device: 0x20, bank: "A", bit: "0b00000000"}, \
                 7: {tech: tech_i2c, device: 0x20, bank: "A", bit: "0b00000000"}, \
                 8: {tech: tech_i2c, device: 0x20, bank: "A", bit: "0b00000000"}, \
                 9: {tech: tech_i2c, device: 0x20, bank: "A", bit: "0b00000000"} }

clock_minutes = {0: {tech: tech_i2c, device: 0x20, bank: "A", bit: "0b10000000"}, \
                 3: {tech: tech_i2c, device: 0x20, bank: "A", bit: "0b01000000"}, \
                 2: {tech: tech_i2c, device: 0x20, bank: "B", bit: "0b00000001"}, \
                 1: {tech: tech_i2c, device: 0x20, bank: "B", bit: "0b00000010"}, \
                 5: {tech: tech_i2c, device: 0x21, bank: "A", bit: "0b10000000"}, \
                 4: {tech: tech_i2c, device: 0x21, bank: "B", bit: "0b00000001"}, \
                 6: {tech: tech_i2c, device: 0x20, bank: "A", bit: "0b00000000"}, \
                 7: {tech: tech_i2c, device: 0x20, bank: "A", bit: "0b00000000"}, \
                 8: {tech: tech_i2c, device: 0x20, bank: "A", bit: "0b00000000"}, \
                 9: {tech: tech_i2c, device: 0x20, bank: "A", bit: "0b00000000"} }

# clock_minutes = ...
# clock_hours   = ...

bits = {}

###############################################################################
# Ports of MCP23x17 ###########################################################
IODIRA      = 0x00 # Pin direction register
IODIRB      = 0x01 # Pin direction register
OLATA       = 0x14 # Register for outputs
OLATB       = 0x15 # Register for outputs

# I2C (MCP23017) ##############################################################
i2c_devices = (0x20, 0x21)    # Addresses of MCP23017 components
i2c         = smbus.SMBus(1)


# SPI (MCP23S17) ##############################################################
spi_devices = (0)   ## TODO: define addresses
spi = spidev.SpiDev()
spi.open(0,1)

# http://erik-bartmann.de/component/attachments/download/23.html
# Pi-Book p 460ff.


###############################################################################
# GetBank #####################################################################
def GetBank(string):
   if (string == "A"):
      return OLATA
   elif (string == "B"):
      return OLATB
   else:
      print "Unknown bank!"
      # Exception!
      return 0x14


###############################################################################
# InitPortExpander ############################################################
# Set port direction to output (0b00000000) ###################################
def InitPortExpander():
   # I2C ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
   for d in i2c_devices:
      i2c.write_byte_data(d, IODIRA, 0b00000000)
      i2c.write_byte_data(d, IODIRB, 0b00000000)

   # SPI +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
   # TODO: for d in spi_devices: 



###############################################################################
# InitBits ####################################################################
def InitBits(pattern):
   global bits

   bits[tech_i2c,0x20,"A"] = pattern
   bits[tech_i2c,0x20,"B"] = pattern
   bits[tech_i2c,0x21,"A"] = pattern
   bits[tech_i2c,0x21,"B"] = pattern



###############################################################################
# WriteBits ###################################################################
def WriteBits():
  for k in bits:
#    print "Tech: ", k[0], "Device: ", k[1], "Bank: ", k[2], "Pattern: ", bits[k]

    if (k[0] == tech_i2c):
       i2c.write_byte_data(k[1], GetBank(k[2]), bits[k])
    # TODO: if (k[0] == tech_spi ...



###############################################################################
# AllOff ######################################################################
def AllOff():
   InitBits(0b00000000)
   WriteBits()



###############################################################################
# Cleanup #####################################################################
def Cleanup():
   AllOff()
   spi.close()



###############################################################################
# Exit ########################################################################
def Exit():
   Cleanup()
   sys.exit()



###############################################################################
# Main ########################################################################
def Main():
   while(1):
      h, m, s = strftime("%H:%M:%S", localtime()).split(":")
      s = int(s) % 10
      m = int(m) % 10
      h = int(h) % 12
      # print s, clock_seconds[s][tech], clock_seconds[s][device], clock_seconds[s][bank], clock_seconds[s][bit]

      AllOff()
      bits[clock_seconds[s][tech], clock_seconds[s][device], clock_seconds[s][bank]]  = int(clock_seconds[s][bit],2)
      bits[clock_seconds[m][tech], clock_seconds[m][device], clock_seconds[m][bank]] |= int(clock_seconds[m][bit],2)
      WriteBits()
      sleep(1)



###############################################################################
###############################################################################
try:
   InitPortExpander()
   Main()

except:
   print(traceback.print_exc())

finally:
   Exit()


