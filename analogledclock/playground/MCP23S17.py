import RPi.GPIO as io
from MCP23x17 import MCP23x17
from SPI_const import SPI_const


# Taken from http://erik-bartmann.de/

class MCP23S17:
   SPI_SLAVE_ADDR_BASE  = 0x40

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


   def send(self, device, addr, data):   # TODO: rename "addr" to "bank"
      # CS aktive (LOW-Aktiv)
      io.output(self.cs, io.LOW)

      self.__sendValue(device|self.SPI_SLAVE_ADDR_BASE)
      self.__sendValue(addr)
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
      self.send(0x00, MCP23x17.IOCONA, 0b00001000) # Set HAEN to 1.
      self.send(0x00, MCP23x17.IOCONB, 0b00001000) # Set HAEN to 1.

      # Set port direction to output (0b00000000)
      for d in self.devices:
         self.send(d, MCP23x17.IODIRA, 0x00)
         self.send(d, MCP23x17.IODIRB, 0x00)

