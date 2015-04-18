#!/usr/bin/python

import smbus
from time import sleep, localtime, strftime


IODIRA = 0x00 # Pin direction register
IODIRB = 0x01 # Pin direction register
OLATA  = 0x14 # Register for outputs
OLATB  = 0x15 # Register for outputs



i2c = smbus.SMBus(1)


tech     = 'tech'
tech_i2c = 'i2c'
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


# clock_minutes = ...
# clock_hours   = ...

bits = {}



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
def InitPortExpander():
   # Portexpander #1, Address 0x20
   i2c.write_byte_data(0x20, IODIRA, 0b00000000)
   i2c.write_byte_data(0x20, IODIRB, 0b00000000)

   # Portexpander #2, Address 0x21
   i2c.write_byte_data(0x21, IODIRA, 0b00000000)
   i2c.write_byte_data(0x21, IODIRB, 0b00000000)



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



###############################################################################
# AllOff ######################################################################
def AllOff():
   InitBits(0b00000000)
   WriteBits()



###############################################################################
# Main ########################################################################
def Main():
   while(1):
      h, m, s = strftime("%H:%M:%S", localtime()).split(":")
      s = int(s) % 10
      m = int(m)
      h = int(h) % 12
      # print s, clock_seconds[s][tech], clock_seconds[s][device], clock_seconds[s][bank], clock_seconds[s][bit]

      bits[clock_seconds[s][tech], clock_seconds[s][device], clock_seconds[s][bank]] = int(clock_seconds[s][bit],2)
      WriteBits()
      sleep(1)
      InitBits(0b00000000)
      WriteBits()



###############################################################################
###############################################################################
InitPortExpander()
InitBits(0b00000000)
WriteBits()
Main()


