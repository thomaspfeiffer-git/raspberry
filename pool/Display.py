# -*- coding: utf-8 -*-
###############################################################################
# Display.py                                                                  #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2019                   #
###############################################################################

"""
TODO
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


class Display (threading.Thread):
    def __init__ (self, data):
        threading.Thread.__init__(self)
        self.data = data
        self.display = SSD1306()

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

        self.draw_line("In:")
        self.draw_line("Out:")
        self.draw_line("Water:")
        self.draw_line("Time: {}".format(time.strftime("%X")))

        self.display.image(self.image)
        self.display.display()

    def off (self):
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

