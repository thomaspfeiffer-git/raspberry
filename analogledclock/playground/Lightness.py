





from time import sleep, localtime, strftime
import threading
import wiringpi2 as wipi

from SPI_const import SPI_const
from MCP3008  import MCP3008


class Lightness (threading.Thread):
   def __init__(self):
      threading.Thread.__init__(self)

      # SPI (MCP3008)
      self.adc = MCP3008(SPI_const.CS0,0)

      # Hardware PWM
      wipi.wiringPiSetupPhys()
      wipi.pinMode(12,2)
      self.running = True

   def run(self):
      while (self.running):
         d = darkness = self.adc.read()
         if (darkness < 512):
            darkness /= 1.5
#         else:
#            darkness *=1.15
         if (darkness >= 1023):
            darkness = 1023
         darkness = int(darkness)
         wipi.pwmWrite(12,1024-darkness)
         print("Darkness: {}/{}".format(d, darkness))
         sleep(0.1)

   def stop(self):
      self.running = False

### eof ###
