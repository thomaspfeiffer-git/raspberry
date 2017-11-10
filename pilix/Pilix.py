#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# Pilix.py                                                                    #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2017                   #
###############################################################################
"""Pilix: my Pi in the sky project:
   control weather balloon"""


# Cam500B is currently not working with a 4.x kernel:
# http://www.friendlyarm.com/Forum/viewtopic.php?f=47&t=1034

# Some ideas on howto solve this:
# https://forum.armbian.com/topic/3225-nanopi-neo-air-cam500b-issue/
# https://github.com/avafinger/ov5640



### usage ###
# nohup ./Pilix.py > ./Logs/pilix.log 2>&1 &


### Packages you might install ###
#
# sudo apt-get install gpsd gpsd-clients python-gps -y
#
# sudo pip3 install Pillow
#
#
# http://flask.pocoo.org/docs/0.12/
#
# http://jinja.pocoo.org/docs/2.9/
# sudo pip3 install Jinja2
#
# http://werkzeug.pocoo.org/docs/0.11/
# sudo pip3 install Werkzeug
#
# http://flask.pocoo.org/docs/0.12/
# sudo pip3 install Flask


import csv
from enum import Enum
from flask import Flask, request
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

from config import CONFIG


V_TemperatureBox     = "Temperature in box"
V_TemperatureOutside = "Temperature outside"
V_Pressure           = "Pressure"
V_Voltage            = "Voltage"
V_RunningOnBattery   = "running on battery"
V_TemperatureCPU     = "Temperature CPU"
V_Timestamp          = "Timestamp"
V_Time               = "Time"
V_GPS_Time           = "GPS Time"
V_GPS_Lon            = "GPS Longitude"
V_GPS_Lat            = "GPS Latitude"
V_GPS_Alt            = "GPS Altitude"
V_GPS_Climb          = "GPS Climb"
V_GPS_Speed          = "GPS Speed"
V_GPS_Track          = "GPS Track"
V_GPS_ErrLon         = "GPS Err Longitude"
V_GPS_ErrLat         = "GPS Err Latitude"
V_GPS_ErrAlt         = "GPS Err Altitude"


app = Flask(__name__)


###############################################################################
# Switch ######################################################################
class Switch (Enum):
    OFF = 0
    ON  = 1


###############################################################################
# Sensors #####################################################################
class Sensors (object):
    v_ref = 8.14

    def __init__ (self):
        self.cpu = CPU()
        self.bmp180 = BMP180()   # air pressure, temperature
        self.pcf8591 = PCF8591() # ADC for measurement of supply voltage

    def read (self):
        timestamp = time.time()
        return{V_TemperatureBox: self.bmp180.read_temperature(),
               V_TemperatureOutside: -22.22,
               V_Pressure: self.bmp180.read_pressure(),
               V_Voltage: self.pcf8591.read(channel=0) / 255.0 * self.v_ref,
               V_TemperatureCPU: self.cpu.read_temperature(),
               V_Timestamp: timestamp,
               V_Time: time.strftime("%X", time.localtime(timestamp))}


###############################################################################
# Camera ######################################################################
class Camera (threading.Thread):
    intervall = CONFIG.Camera.Intervall
    def __init__ (self):
        threading.Thread.__init__(self)
        self.statusled = StatusLED(CONFIG.PIN.LED_Picture)
        self._takingPictures = False
        self._running = True

    def run (self):
        while self._running:
            if self._takingPictures:
                for _ in range(self.intervall*10):
                    if self._running:
                        time.sleep(0.1)
                self.statusled.flash()
                Log("taking picture")
            else:
                time.sleep(0.1)

    def toggle_takePictures (self):
        self._takingPictures = not self._takingPictures
        Log("Camera: {}".format(self._takingPictures))
        if self._takingPictures:
            blinks = 4
        else:
            blinks = 2
        for _ in range(blinks):
            self.statusled.flash()
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

        self.draw_line("Temp: {} °C".format(data[V_TemperatureBox]))
        self.draw_line("Press: {} hPa".format(data[V_Pressure] / 100.0))
        self.draw_line("Voltage: {:.2f} V".format(data[V_Voltage]))
        self.draw_line("X: {} Y: {}".format(data[V_GPS_Lon], data[V_GPS_Lat]))
        self.draw_line("Time: {}".format(data[V_Time]))

        self.display.image(self.image)
        self.display.display()

    def off (self):
        self.display.clear()
        self.display.display()


###############################################################################
# CSV #########################################################################
class CSV (object):
    fieldnames = [V_Time, V_TemperatureBox, V_TemperatureOutside, 
                  V_Pressure, V_Voltage, V_RunningOnBattery, V_TemperatureCPU, 
                  V_Timestamp, V_GPS_Time, V_GPS_Lon, V_GPS_Lat, V_GPS_Alt, 
                  V_GPS_Climb, V_GPS_Speed, V_GPS_Track, V_GPS_ErrLon, 
                  V_GPS_ErrLat, V_GPS_ErrAlt]

    def __init__ (self):
        with open(CONFIG.File.csv, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames, delimiter=';')
            writer.writeheader()

    def write (self, data):
        with open(CONFIG.File.csv, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames, delimiter=';')
            writer.writerow(data)


###############################################################################
# Control #####################################################################
class Control (threading.Thread):
    def __init__ (self):
        threading.Thread.__init__(self)
        self.csv       = CSV()
        self.display   = Display()
        self.sensors   = Sensors()
        self.statusled = StatusLED(CONFIG.PIN.LED_Status)

        self.running_on_battery = False
        self._running = True


    def get_gps_data (self):
        return {V_GPS_Time: "17:17:17",
                V_GPS_Lon: "18.18",
                V_GPS_Lat: "48.48",
                V_GPS_Alt: "222",
                V_GPS_Climb: "10",
                V_GPS_Speed: "100",
                V_GPS_Track: "47",
                V_GPS_ErrLon: "3",
                V_GPS_ErrLat: "4",
                V_GPS_ErrAlt: "5"}

    def run (self):
        while self._running:
            data = self.sensors.read()
            data[V_RunningOnBattery] = self.running_on_battery
            data.appand(self.get_gps_data())

            self.display.print(data)
            self.csv.write(data)
            for _ in range(15):  # sleep for 15 x 2 = 30 seconds
                if not self._running:
                    break

                for i in range(20):  # flash LED every two seconds (heartbeat)
                    if not self._running:
                        break
                    if i == 0:
                        self.statusled.flash()
                    time.sleep(0.1)

        self.display.off()

    def stop (self):
        self._running = False


###############################################################################
# Flask stuff #################################################################
@app.route('/shutdown')
def API_Shutdown ():
    Log("Shutdown requested")
    return "shutdown ok"

@app.route('/toggle')
def API_Toggle ():
    Log("Camera: toggle requested")
    camera.toggle_takePictures()
    return "toggle ok"

@app.route('/battery')
def API_Battery ():                  # looks weird, but is fail safe
    running_on_battery = not (request.args.get('enabled', 'False') != "True")
    Log("Running on battery: {}".format(running_on_battery))
    control.running_on_battery = running_on_battery
    return "battery ok"


###############################################################################
# Exit ########################################################################
def shutdown_application ():
    """cleanup stuff"""
    Log("stopping application")
    control.stop()
    control.join()
    camera.stop()
    camera.join()
    Log("application stopped")
    sys.exit(0)


###############################################################################
## main #######################################################################
if __name__ == "__main__":
    shutdown = Shutdown(shutdown_func=shutdown_application)

    camera  = Camera()
    camera.start()

    control = Control()
    control.start()

    app.run(host="0.0.0.0")

# eof #
   
