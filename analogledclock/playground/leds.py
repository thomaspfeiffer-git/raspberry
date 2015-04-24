#!/usr/bin/python

import RPi.GPIO as io
import signal
import smbus
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
                 6: {tech: tech_i2c, device: 0x20, bank: "A", bit: "0b00100000"}, \
                 7: {tech: tech_i2c, device: 0x20, bank: "A", bit: "0b00010000"}, \
                 8: {tech: tech_i2c, device: 0x20, bank: "A", bit: "0b00001000"}, \
                 9: {tech: tech_i2c, device: 0x20, bank: "A", bit: "0b00000100"} }

clock_minutes = {0: {tech: tech_i2c, device: 0x20, bank: "A", bit: "0b10000000"}, \
                 3: {tech: tech_i2c, device: 0x20, bank: "A", bit: "0b01000000"}, \
                 2: {tech: tech_i2c, device: 0x20, bank: "B", bit: "0b00000001"}, \
                 1: {tech: tech_i2c, device: 0x20, bank: "B", bit: "0b00000010"}, \
                 5: {tech: tech_i2c, device: 0x21, bank: "A", bit: "0b10000000"}, \
                 4: {tech: tech_i2c, device: 0x21, bank: "B", bit: "0b00000001"}, \
                 6: {tech: tech_i2c, device: 0x20, bank: "A", bit: "0b00000010"}, \
                 7: {tech: tech_i2c, device: 0x20, bank: "A", bit: "0b00000001"}, \
                 8: {tech: tech_i2c, device: 0x20, bank: "A", bit: "0b00000010"}, \
                 9: {tech: tech_i2c, device: 0x20, bank: "A", bit: "0b00000001"} }

clock_hours   = {0: {tech: tech_spi, device: 0x00, bank: "A", bit: "0b00000001"}, \
                 1: {tech: tech_spi, device: 0x00, bank: "A", bit: "0b00000010"}, \
                 2: {tech: tech_spi, device: 0x00, bank: "A", bit: "0b00000100"}, \
                 3: {tech: tech_spi, device: 0x00, bank: "B", bit: "0b10000000"}, \
                 4: {tech: tech_spi, device: 0x00, bank: "B", bit: "0b01000000"}, \
                 5: {tech: tech_spi, device: 0x00, bank: "B", bit: "0b00100000"}, \
                 6: {tech: tech_spi, device: 0x00, bank: "A", bit: "0b00000011"}, \
                 7: {tech: tech_spi, device: 0x00, bank: "A", bit: "0b00000101"}, \
                 8: {tech: tech_spi, device: 0x00, bank: "A", bit: "0b00000110"}, \
                 9: {tech: tech_spi, device: 0x00, bank: "B", bit: "0b11000000"}, \
                10: {tech: tech_spi, device: 0x00, bank: "B", bit: "0b10100000"}, \
                11: {tech: tech_spi, device: 0x00, bank: "B", bit: "0b01100000"}, \
                12: {tech: tech_spi, device: 0x00, bank: "A", bit: "0b00000001"}, \
                13: {tech: tech_spi, device: 0x00, bank: "A", bit: "0b00000010"}, \
                14: {tech: tech_spi, device: 0x00, bank: "A", bit: "0b00000100"}, \
                15: {tech: tech_spi, device: 0x00, bank: "B", bit: "0b10000000"}, \
                16: {tech: tech_spi, device: 0x00, bank: "B", bit: "0b01000000"}, \
                17: {tech: tech_spi, device: 0x00, bank: "B", bit: "0b00100000"}, \
                18: {tech: tech_spi, device: 0x00, bank: "A", bit: "0b00000111"}, \
                19: {tech: tech_spi, device: 0x00, bank: "A", bit: "0b00000011"}, \
                20: {tech: tech_spi, device: 0x00, bank: "A", bit: "0b00000101"}, \
                21: {tech: tech_spi, device: 0x00, bank: "B", bit: "0b11100000"}, \
                22: {tech: tech_spi, device: 0x02, bank: "A", bit: "0b00000010"}, \
                23: {tech: tech_spi, device: 0x02, bank: "A", bit: "0b00000001"} }

bits = {}

###############################################################################
# Ports of MCP23x17 ###########################################################
IODIRA      = 0x00 # Pin direction register
IODIRB      = 0x01 # Pin direction register
IOCONA      = 0x0A # MCP23S17 needs hardware addressing explicitly enabled.
IOCONB      = 0x0B # MCP23S17 needs hardware addressing explicitly enabled.
OLATA       = 0x14 # Register for outputs
OLATB       = 0x15 # Register for outputs

# I2C (MCP23017) ##############################################################
i2c_devices = (0x20, 0x21)    # Addresses of MCP23017 components
i2c         = smbus.SMBus(1)

# SPI (MCP23S17) ##############################################################
SPI_SLAVE_ADDR_BASE  = 0x40
spi_devices          = (0x00, 0x02)

SPI_SCLK = 23
SPI_MOSI = 19
SPI_MISO = 21
SPI_CS = 26



###############################################################################
def sendValue(value):
    v = value

    for i in range(8):
       if (v & 0x80):
            io.output(SPI_MOSI, io.HIGH)
       else:
            io.output(SPI_MOSI, io.LOW)

        # Negative Flanke des Clocksignals generieren
       io.output(SPI_SCLK, io.HIGH)
       io.output(SPI_SCLK, io.LOW)
       v <<= 1 # Bitfolge eine Position nach links schieben



###############################################################################
def sendSPI(device, addr, data):
    # CS aktive (LOW-Aktiv)
    io.output(SPI_CS, io.LOW)

    sendValue(device|SPI_SLAVE_ADDR_BASE) 
    sendValue(addr)                            # Adresse senden
    sendValue(data)                            # Daten senden

    # CS nicht aktiv
    io.output(SPI_CS, io.HIGH)



###############################################################################
# InitPortExpander ############################################################
# Set port direction to output (0b00000000) ###################################
def InitPortExpander():
   # I2C ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
   for d in i2c_devices:
      i2c.write_byte_data(d, IODIRA, 0b00000000)
      i2c.write_byte_data(d, IODIRB, 0b00000000)

   # SPI +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
   io.setmode(io.BOARD)
   io.setwarnings(False)

   # Pin-Programmierung
   io.setup(SPI_SCLK, io.OUT)
   io.setup(SPI_MOSI, io.OUT)
   io.setup(SPI_MISO, io.IN)
   io.setup(SPI_CS,   io.OUT)

   # Pegel vorbereiten
   io.output(SPI_CS,   io.HIGH)
   io.output(SPI_SCLK, io.LOW)
   
   # MCP23S17 needs hardware addressing explicitly enabled.
   sendSPI(0x00, IOCONA, 0b00001000)
   sendSPI(0x00, IOCONB, 0b00001000)

   # TODO:
   # for d in spi_devices:
   # set port direction to output
   sendSPI(0x00, IODIRA, 0x00)
   sendSPI(0x00, IODIRB, 0x00)
   sendSPI(0x02, IODIRA, 0x00)
   sendSPI(0x02, IODIRB, 0x00)

    

###############################################################################
# InitBits ####################################################################
def InitBits(pattern):
   global bits

   bits[tech_i2c,0x20,"A"] = pattern   # TODO: for ...
   bits[tech_i2c,0x20,"B"] = pattern
   bits[tech_i2c,0x21,"A"] = pattern
   bits[tech_i2c,0x21,"B"] = pattern
   bits[tech_spi,0x00,"A"] = pattern
   bits[tech_spi,0x00,"B"] = pattern
   bits[tech_spi,0x02,"A"] = pattern
   bits[tech_spi,0x02,"B"] = pattern



###############################################################################
# GetBank #####################################################################
def GetBank(string):
   if (string == "A"):
      return OLATA
   elif (string == "B"):
      return OLATB
   else:
      print "Unknown bank!"
      # TODO: Exception!
      return OLATA



###############################################################################
# WriteBits ###################################################################
def WriteBits():
  for k in bits:
#    print "Tech: ", k[0], "Device: ", k[1], "Bank: ", k[2], "Pattern: ", bits[k]

    if (k[0] == tech_i2c):
       i2c.write_byte_data(k[1], GetBank(k[2]), bits[k])
    elif (k[0] == tech_spi):
       sendSPI(k[1], GetBank(k[2]), bits[k]) 
    else:
       print "Unknown tech!"
       # TODO: Exception!
       return OLATA



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
   sys.exit()

def _Exit(s,f):
   print "_Exit"   # Wird das wirklich aufgerufen?
   Exit()


###############################################################################
# Main ########################################################################
def Main():
   while(1):
      h, m, s = strftime("%H:%M:%S", localtime()).split(":")
      s = int(s) % 10
      m = int(m) % 10
      h = int(h)
      # print s, clock_seconds[s][tech], clock_seconds[s][device], clock_seconds[s][bank], clock_seconds[s][bit]
      # print m, clock_minutes[m][tech], clock_minutes[m][device], clock_minutes[m][bank], clock_minutes[m][bit]
      # print h, clock_hours[h][tech], clock_hours[h][device], clock_hours[h][bank], clock_hours[h][bit]

      InitBits(0b00000000)
      # In this project, seconds and minutes share the same LEDs. Therefore
      # i've to |= the bit array.
      bits[clock_seconds[s][tech], clock_seconds[s][device], clock_seconds[s][bank]]  = int(clock_seconds[s][bit],2)
      bits[clock_seconds[m][tech], clock_seconds[m][device], clock_seconds[m][bank]] |= int(clock_seconds[m][bit],2)
      bits[clock_hours[h][tech], clock_hours[h][device], clock_hours[h][bank]] = int(clock_hours[h][bit],2)
      WriteBits()
      sleep(1)



###############################################################################
###############################################################################
signal.signal(signal.SIGTERM, _Exit)
try:
   InitPortExpander()
   Main()

except KeyboardInterrupt:
   Exit()

except SystemExit:                  # Done in signal handler (method _Exit()) #
   pass

except:
   print(traceback.print_exc())

finally:        # All cleanup is done in KeyboardInterrupt or signal handler. #
   pass


