###############################################################################################
# MCP23017                                                                                    #
# Communication with MCP23S17                                                                 #
# (c) https://github.com/thomaspfeiffer-git 2015                                              #
###############################################################################################

import spidev

import RPi.GPIO as io
from MCP23x17 import MCP23x17
from SPI_const import SPI_const


class MCP23S17_xfer:
   MCP23S17_SLAVE_ADDR_BASE = 0x40
   MCP23S17_SLAVE_WRITE     = 0x00
   MCP23S17_SLAVE_READ      = 0x01

   def send (self, device, register, data):
      d = device << 1
      self.spi.xfer2([d|self.MCP23S17_SLAVE_ADDR_BASE|self.MCP23S17_SLAVE_WRITE,register,data])


   def __init__ (self, cs, devices):
      self.cs = cs
      # self.cs = 0 if (cs == SPI_const.CS0) else 1 
      self.devices = devices

      self.spi = spidev.SpiDev()
      self.spi.open(0,1)  # TODO: cs

      # MCP23S17 needs hardware addressing explicitly enabled.
      for d in self.devices:
         self.send(d, MCP23x17.IOCONA, 0b00001000) # Set HAEN to 1.
         self.send(d, MCP23x17.IOCONB, 0b00001000) # Set HAEN to 1.

      # Set port direction to output (0b00000000)
      for d in self.devices:
         self.send(d, MCP23x17.IODIRA, 0x00)
         self.send(d, MCP23x17.IODIRB, 0x00)


   def close (self):
      self.spi.close()



class MCP23S17:
   SPI_SLAVE_ADDR_BASE  = 0x40
   SPI_SLAVE_READ       = 0x01
   SPI_SLAVE_WRITE      = 0x00

   def __sendValue(self, value):
     v = value

     for i in range(8):
        if (v & 0x80):
             io.output(SPI_const.MOSI, io.HIGH)
        else:
             io.output(SPI_const.MOSI, io.LOW)

         # Negative Flanke des Clocksignals generieren
        io.output(SPI_const.SCLK, io.HIGH)
        io.output(SPI_const.SCLK, io.LOW)
        v <<= 1 # Bitfolge eine Position nach links schieben


   def send(self, device, bank, data):
      # CS aktive (LOW-Aktiv)
      io.output(self.cs, io.LOW)

      d = device << 1
      self.__sendValue(d|self.SPI_SLAVE_ADDR_BASE|self.SPI_SLAVE_WRITE) 
      self.__sendValue(bank) 
      self.__sendValue(data)

      # CS nicht aktiv
      io.output(self.cs, io.HIGH)



   def __init__ (self, cs, devices):
      self.devices = devices
      self.cs      = cs

      io.setmode(io.BOARD)
      io.setwarnings(False)

      # Pin-Programmierung
      io.setup(SPI_const.SCLK, io.OUT)
      io.setup(SPI_const.MOSI, io.OUT)
      io.setup(SPI_const.MISO, io.IN)
      io.setup(self.cs,   io.OUT)

      # Pegel vorbereiten
      io.output(self.cs,   io.HIGH)
      io.output(SPI_const.SCLK, io.LOW)

      # MCP23S17 needs hardware addressing explicitly enabled.
      for d in self.devices:
         self.send(d, MCP23x17.IOCONA, 0b00001000) # Set HAEN to 1.
         self.send(d, MCP23x17.IOCONB, 0b00001000) # Set HAEN to 1.
         # self.send(d, MCP23x17.IOCONA, 0x28) # Set HAEN to 1.
         # self.send(d, MCP23x17.IOCONB, 0x28) # Set HAEN to 1.

      # Set port direction to output (0b00000000)
      for d in self.devices:
         self.send(d, MCP23x17.IODIRA, 0x00)
         self.send(d, MCP23x17.IODIRB, 0x00)


### eof ###

