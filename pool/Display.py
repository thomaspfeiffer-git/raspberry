# -*- coding: utf-8 -*-
###############################################################################
# Display.py                                                                  #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2019                   #
###############################################################################

"""
Displays most important data on an SSD1306.
"""

import sys
import threading
import time

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


sys.path.append("../libs/")
from actuators.SSD1306 import SSD1306
from Logging import Log


###############################################################################
# Display #####################################################################
class Display (threading.Thread):
    def __init__ (self, data, lock):
        threading.Thread.__init__(self)
        self.data = data
        self.__lock = lock
        self.display = SSD1306()

        with self.__lock:
            self.display.begin()
            self.off()

        self.xpos = 6
        self.ypos = 2

        self.image = Image.new('1', (self.display.width, self.display.height))
        self.draw  = ImageDraw.Draw(self.image)
        self.font  = ImageFont.load_default()
        (_, self.fontheight) = self.font.getsize("A")

        self._running = True

    def draw_line (self, text):
        self.draw.text((self.xpos, self.y), text, font=self.font, fill=0)
        self.y += self.fontheight

    def print (self):
        self.draw.rectangle((0,0,self.display.width,self.display.height),
                            outline=0, fill=255)
        self.y = self.ypos

        if self.data.valid:
            self.draw_line("I: {0.airin_temp:.1f} °C / {0.airin_humidity:.0f} % rF".format(self.data))
            self.draw_line("O: {0.airout_temp:.1f} °C / {0.airout_humidity:.0f} % rF".format(self.data))
            self.draw_line("Water: {0.water_temp:.1f} °C".format(self.data))
            self.draw_line("Time: {}".format(time.strftime("%X")))

        with self.__lock:
            self.display.image(self.image)
            self.display.display()

    def off (self):
        with self.__lock:
            self.display.clear()
            self.display.display()

    def run (self):
        while self._running:
            self.print()

            for _ in range(10):
                if not self._running:
                    break
                time.sleep(0.1)    
        self.off()        

    def stop (self):
        self._running = False

# eof #

