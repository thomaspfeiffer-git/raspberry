import RPi.GPIO as io


class MCP3008:
   SCLK       = 23  # Serial-Clock
   MOSI       = 19  # Master-Out-Slave-In
   MISO       = 21  # Master-In-Slave-Out
   CS         = 24  # Chip-Select

   def __init__(self, channel):
      self.channel = channel

      io.setmode(io.BOARD)
      io.setwarnings(False)

      io.setup(self.SCLK, io.OUT)
      io.setup(self.MOSI, io.OUT)
      io.setup(self.MISO, io.IN)
      io.setup(self.CS,   io.OUT)


   def read(self):
      # Negative Flanke des CS-Signals generieren
      io.output(self.CS,   io.HIGH)
      io.output(self.CS,   io.LOW)
      io.output(self.SCLK, io.LOW)   
      sendCMD = self.channel
      sendCMD |= 0b00011000 # Entspricht 0x18 (1: Startbit, 1: Single/ended)
      # Senden der Bitkombination (Es finden nur 5 Bits Beruecksichtigung)
      for i in range(5):
         if(sendCMD & 0x10): # Bit an Position 4 pruefen.
            io.output(self.MOSI, io.HIGH)
         else:
            io.output(self.MOSI, io.LOW)
         # Negative Flanke des Clock-Signals generieren
         io.output(self.SCLK, io.HIGH)
         io.output(self.SCLK, io.LOW)
         sendCMD <<= 1 # Bitfolge eine Position nach links schieben
      # Empfangen der Daten des AD-Wandlers
      adcValue = 0 # Reset des gelesenen Wertes
      for i in range(11):
         # Negative Flanke des Clock-Signals generieren
         io.output(self.SCLK, io.HIGH)
         io.output(self.SCLK, io.LOW)
         adcValue <<= 1 # Bitfolge 1 Position nach links schieben
         if(io.input(self.MISO)):
            adcValue |=0x01
      return adcValue



