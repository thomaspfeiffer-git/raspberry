#!/usr/bin/python

import signal
from time import sleep, localtime, strftime
import sys
import traceback
import wiringpi2 as wipi


from SPI_const import SPI_const
from MCP23x17 import MCP23x17
from MCP23017 import MCP23017
from MCP23S17 import MCP23S17
from MCP3008  import MCP3008


tech     = 'tech'
tech_i2c = 'i2c'
tech_spi = 'spi'
device   = 'device'
bank     = 'bank'
bit      = 'bit'


# I2C (MCP23017)
i2c_devices = (0x20, 0x21)    # Addresses of MCP23017 components
i2c         = MCP23017(i2c_devices)

# SPI (MCP23S17) 
spi_devices = (0x00, 0x02)    # Addresses of MCP23S17 components
spi         = MCP23S17(SPI_const.CS1,spi_devices)

# SPI (MCP3008)
adc = MCP3008(SPI_const.CS0,0)

# PWM (Wiring PI)
wipi.wiringPiSetupPhys()
wipi.pinMode(12,2)


clock_seconds = {0: {tech: i2c, device: 0x20, bank: "A", bit: "0b10000000"}, \
                 3: {tech: i2c, device: 0x20, bank: "A", bit: "0b01000000"}, \
                 2: {tech: i2c, device: 0x20, bank: "B", bit: "0b00000001"}, \
                 1: {tech: i2c, device: 0x20, bank: "B", bit: "0b00000010"}, \
                 5: {tech: i2c, device: 0x21, bank: "A", bit: "0b10000000"}, \
                 4: {tech: i2c, device: 0x21, bank: "B", bit: "0b00000001"}, \
                 6: {tech: i2c, device: 0x20, bank: "A", bit: "0b00100000"}, \
                 7: {tech: i2c, device: 0x20, bank: "A", bit: "0b00010000"}, \
                 8: {tech: i2c, device: 0x20, bank: "A", bit: "0b00001000"}, \
                 9: {tech: i2c, device: 0x20, bank: "A", bit: "0b00000100"} }

clock_minutes = {0: {tech: i2c, device: 0x20, bank: "A", bit: "0b10000000"}, \
                 3: {tech: i2c, device: 0x20, bank: "A", bit: "0b01000000"}, \
                 2: {tech: i2c, device: 0x20, bank: "B", bit: "0b00000001"}, \
                 1: {tech: i2c, device: 0x20, bank: "B", bit: "0b00000010"}, \
                 5: {tech: i2c, device: 0x21, bank: "A", bit: "0b10000000"}, \
                 4: {tech: i2c, device: 0x21, bank: "B", bit: "0b00000001"}, \
                 6: {tech: i2c, device: 0x20, bank: "A", bit: "0b00000010"}, \
                 7: {tech: i2c, device: 0x20, bank: "A", bit: "0b00000001"}, \
                 8: {tech: i2c, device: 0x20, bank: "A", bit: "0b00000010"}, \
                 9: {tech: i2c, device: 0x20, bank: "A", bit: "0b00000001"} }

clock_hours   = {0: {tech: spi, device: 0x00, bank: "A", bit: "0b00000001"}, \
                 1: {tech: spi, device: 0x00, bank: "A", bit: "0b00000010"}, \
                 2: {tech: spi, device: 0x00, bank: "A", bit: "0b00000100"}, \
                 3: {tech: spi, device: 0x00, bank: "B", bit: "0b10000000"}, \
                 4: {tech: spi, device: 0x00, bank: "B", bit: "0b01000000"}, \
                 5: {tech: spi, device: 0x00, bank: "B", bit: "0b00100000"}, \
                 6: {tech: spi, device: 0x00, bank: "A", bit: "0b00000011"}, \
                 7: {tech: spi, device: 0x00, bank: "A", bit: "0b00000101"}, \
                 8: {tech: spi, device: 0x00, bank: "A", bit: "0b00000110"}, \
                 9: {tech: spi, device: 0x00, bank: "B", bit: "0b11000000"}, \
                10: {tech: spi, device: 0x00, bank: "B", bit: "0b10100000"}, \
                11: {tech: spi, device: 0x00, bank: "B", bit: "0b01100000"}, \
                12: {tech: spi, device: 0x00, bank: "A", bit: "0b00000001"}, \
                13: {tech: spi, device: 0x00, bank: "A", bit: "0b00000010"}, \
                14: {tech: spi, device: 0x00, bank: "A", bit: "0b00000100"}, \
                15: {tech: spi, device: 0x00, bank: "B", bit: "0b10000000"}, \
                16: {tech: spi, device: 0x00, bank: "B", bit: "0b01000000"}, \
                17: {tech: spi, device: 0x00, bank: "B", bit: "0b00100000"}, \
                18: {tech: spi, device: 0x00, bank: "A", bit: "0b00000111"}, \
                19: {tech: spi, device: 0x00, bank: "A", bit: "0b00000011"}, \
                20: {tech: spi, device: 0x00, bank: "A", bit: "0b00000101"}, \
                21: {tech: spi, device: 0x00, bank: "B", bit: "0b11100000"}, \
                22: {tech: spi, device: 0x02, bank: "A", bit: "0b00000010"}, \
                23: {tech: spi, device: 0x02, bank: "A", bit: "0b00000001"} }

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
      print "Unknown bank!"
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
   # TODO: GPIO.cleanup()
   print "Exit"
   sys.exit()

def _Exit(s,f):
   print "_Exit"   # Wird das wirklich aufgerufen?
   Exit()


###############################################################################
# Main ########################################################################
def Main():
   while(1):
      darkness = adc.read()
      if (darkness < 512):
         darkness /= 1.5
#      else:
#         darkness *=1.15
      if (darkness >= 1023):
         darkness = 1023 
      darkness = int(darkness)
#      print "Darkness: ", darkness
      wipi.pwmWrite(12,1024-darkness)

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
   Main()

except KeyboardInterrupt:
   Exit()

except SystemExit:                  # Done in signal handler (method _Exit()) #
   pass

except:
   print(traceback.print_exc())

finally:        # All cleanup is done in KeyboardInterrupt or signal handler. #
   pass


