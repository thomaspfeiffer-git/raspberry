#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# Felix.py                                                                    #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2017                   #
###############################################################################
"""Felix: my Pi in the sky project:
   control weather balloon"""


### usage ###
# nohup ./Felix.py > felix.log 2>&1 &

# Packages you might install
# sudo pip3 install Pillow


from enum import Enum
import subprocess
import sys
import threading
import time

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

sys.path.append("../libs/")
from i2c import I2C
from Logging import Log
from Shutdown import Shutdown

from actuators.SSD1306 import SSD1306
from sensors.CPU import CPU
from sensors.BMP180 import BMP180
from sensors.PCF8591 import PCF8591


pin_LED_Status  = 23
pin_LED_Picture = 24


###############################################################################
# Switch ######################################################################
class Switch (Enum):
    OFF = 0
    ON  = 1


###############################################################################
# Data ########################################################################
class Data (object):
    def __init__ (self, temperature, pressure, voltage, t_cpu, timestamp):
        self.temperature = temperature
        self.pressure    = pressure
        self.voltage     = voltage
        self.t_cpu       = t_cpu
        self.timestamp   = timestamp


###############################################################################
# Sensors #####################################################################
class Sensors (object):
    v_ref = 3.3

    def __init__ (self):
        self.cpu = CPU()
        self.bmp180 = BMP180()   # air pressure, temperature
        self.pcf8591 = PCF8591() # ADC for measurement of supply voltage

    def read (self):
        return Data(temperature = self.bmp180.read_temperature(),
                    pressure    = self.bmp180.read_pressure(),
                    voltage     = self.pcf8591.read(channel=0) / 255.0 * self.v_ref,
                    t_cpu       = self.cpu.read_temperature(),
                    timestamp   = time.strftime("%X"))


###############################################################################
# Camera ######################################################################
class Camera (threading.Thread):
    intervall = 30   # take a picture every 30 seconds
    def __init__ (self):
        threading.Thread.__init__(self)
        self.statusled = StatusLED(pin_LED_Picture)
        self._running = True

    def run (self):
        while self._running:
            self.statusled.flash()
            for _ in range(self.intervall*10):
                if self._running:
                    time.sleep(0.1)

    def stop (self):
        self._running = False


###############################################################################
# StatusLED ###################################################################
class StatusLED (object):
    def __init__ (self, pin):
        self.__pin = "{}".format(pin)
        # FriendlyArm's WiringPI lib does not support python3.
        # http://www.friendlyarm.com/Forum/viewtopic.php?f=47&t=921
        # Therefore i use shell commands.
        subprocess.run(["gpio", "-1", "mode", self.__pin, "output"], check=True)
        self.__last = None
        self.off()

    def io_write (self, status):
        subprocess.run(["gpio", "-1", "write", self.__pin, status], check=True)

    def on (self):
        if self.__last != Switch.ON:
            self.io_write("1")
            self.__last = Switch.ON

    def off (self):
        if self.__last != Switch.OFF:
            self.io_write("0")
            self.__last = Switch.OFF

    def flash (self):
        self.on()
        self.off()


###############################################################################
# Display #####################################################################
class Display (object):
    def __init__ (self):
        self.display = SSD1306()
 
        self.display.begin()
        self.off()

        self.xpos = 6
        self.ypos = 2

        self.image = Image.new('1', (self.display.width, self.display.height))
        self.draw  = ImageDraw.Draw(self.image)
        self.font  = ImageFont.load_default()
        (_, self.fontheight) = self.font.getsize("A")

    def draw_line (self, text):
        self.draw.text((self.xpos, self.y), text, font=self.font, fill=0)
        self.y += self.fontheight

    def print (self, data):
        self.draw.rectangle((0,0,self.display.width,self.display.height),
                            outline=0, fill=255)
        self.y = self.ypos

        self.draw_line("Temp: {} °C".format(data.temperature))
        self.draw_line("Press: {} hPa".format(data.pressure / 100.0))
        self.draw_line("Battery: {:.2f} V".format(data.voltage))
        self.draw_line("Temp CPU: {} °C".format(data.t_cpu))
        self.draw_line("Time: {}".format(data.timestamp))

        self.display.image(self.image)
        self.display.display()

    def off (self):
        self.display.clear()
        self.display.display()


###############################################################################
# Exit ########################################################################
def shutdown_application ():
    """cleanup stuff"""
    camera.stop()
    camera.join()
    display.off()
    sys.exit(0)


###############################################################################
## main #######################################################################
if __name__ == "__main__":
    shutdown = Shutdown(shutdown_func=shutdown_application)

    display = Display()
    sensors = Sensors()
    camera  = Camera()
    camera.start()
    LED_StatusWorking = StatusLED(pin_LED_Status)

    while True:
        data = sensors.read()
        display.print(data)
        for _ in range(10):
            LED_StatusWorking.flash()
            time.sleep(2)

# eof #
   
