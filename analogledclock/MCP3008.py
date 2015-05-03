###############################################################################################
# MCP23017                                                                                    #
# Communication with MCP3008                                                                  #
# Taken from http://erik-bartmann.de/                                                         #
# (c) https://github.com/thomaspfeiffer-git May 2015                                          #
###############################################################################################

import RPi.GPIO as io
from SPI_const import SPI_const

class MCP3008:
   def __init__(self, cs, channel):
      self.channel = channel
      self.cs      = cs

      io.setmode(io.BOARD)
      io.setwarnings(False)

      io.setup(SPI_const.SCLK, io.OUT)
      io.setup(SPI_const.MOSI, io.OUT)
      io.setup(SPI_const.MISO, io.IN)
      io.setup(self.cs, io.OUT)


   def read(self):
      # Negative Flanke des CS-Signals generieren
      io.output(self.cs, io.HIGH)
      io.output(self.cs, io.LOW)
      io.output(SPI_const.SCLK, io.LOW)   

      sendCMD = self.channel
      sendCMD |= 0b00011000 # Entspricht 0x18 (1: Startbit, 1: Single/ended)
      # Senden der Bitkombination (Es finden nur 5 Bits Beruecksichtigung)
      for i in range(5):
         if(sendCMD & 0x10): # Bit an Position 4 pruefen.
            io.output(SPI_const.MOSI, io.HIGH)
         else:
            io.output(SPI_const.MOSI, io.LOW)
         # Negative Flanke des Clock-Signals generieren
         io.output(SPI_const.SCLK, io.HIGH)
         io.output(SPI_const.SCLK, io.LOW)
         sendCMD <<= 1 # Bitfolge eine Position nach links schieben

      # Empfangen der Daten des AD-Wandlers
      adcValue = 0 # Reset des gelesenen Wertes
      for i in range(11):
         # Negative Flanke des Clock-Signals generieren
         io.output(SPI_const.SCLK, io.HIGH)
         io.output(SPI_const.SCLK, io.LOW)
         adcValue <<= 1 # Bitfolge 1 Position nach links schieben
         if(io.input(SPI_const.MISO)):
            adcValue |=0x01
      return adcValue


### eof ###
