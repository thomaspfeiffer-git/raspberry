import RPi.GPIO as io
from MCP23x17 import MCP23x17

class MCP23S17:
   SPI_SLAVE_ADDR_BASE  = 0x40

   SPI_SCLK = 23
   SPI_MOSI = 19
   SPI_MISO = 21
   SPI_CS = 26

   def __sendValue(self, value):
     v = value

     for i in range(8):
        if (v & 0x80):
             io.output(self.SPI_MOSI, io.HIGH)
        else:
             io.output(self.SPI_MOSI, io.LOW)

         # Negative Flanke des Clocksignals generieren
        io.output(self.SPI_SCLK, io.HIGH)
        io.output(self.SPI_SCLK, io.LOW)
        v <<= 1 # Bitfolge eine Position nach links schieben



   def send(self, device, addr, data):   # TODO: rename "addr" to "bank"
      # CS aktive (LOW-Aktiv)
      io.output(self.SPI_CS, io.LOW)

      self.__sendValue(device|self.SPI_SLAVE_ADDR_BASE)
      self.__sendValue(addr)
      self.__sendValue(data)

      # CS nicht aktiv
      io.output(self.SPI_CS, io.HIGH)



   def __init__ (self, devices):
      self.devices = devices

      io.setmode(io.BOARD)
      io.setwarnings(False)

      # Pin-Programmierung
      io.setup(self.SPI_SCLK, io.OUT)
      io.setup(self.SPI_MOSI, io.OUT)
      io.setup(self.SPI_MISO, io.IN)
      io.setup(self.SPI_CS,   io.OUT)

      # Pegel vorbereiten
      io.output(self.SPI_CS,   io.HIGH)
      io.output(self.SPI_SCLK, io.LOW)

      # MCP23S17 needs hardware addressing explicitly enabled.
      self.send(0x00, MCP23x17.IOCONA, 0b00001000) # Set HAEN to 1.
      self.send(0x00, MCP23x17.IOCONB, 0b00001000) # Set HAEN to 1.

      # Set port direction to output (0b00000000)
      for d in self.devices:
         self.send(d, MCP23x17.IODIRA, 0x00)
         self.send(d, MCP23x17.IODIRB, 0x00)

