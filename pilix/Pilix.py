#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# Pilix.py                                                                    #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2017                   #
###############################################################################
"""Pilix: my Pi in the sky project:
   control weather balloon"""


### usage ###
# nohup ./Pilix.py > ./Logs/pilix.log 2>&1 &


# TODO
# - Camera
# - Sensor DS18B20


### Packages you might need to install ###
#
# --- GPS ---
# sudo apt-get install gpsd gpsd-clients python-gps -y
# sudo -H pip3 install gps3
#
# howto start and test gps:
# sudo systemctl stop gpsd.socket
# sudo systemctl disable gpsd.socket
# sudo gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock
#
# cgps -s
#
#
# --- Display ---
# sudo apt-get install libjpeg8-dev -y
# sudo pip3 install Pillow
#
#
# --- Flask ---
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
from gps3.agps3threaded import AGPS3mechanism
from enum import Enum
from flask import Flask, request
import RPi.GPIO as io
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
        self.piccount = 0
        self._takingPictures = False
        self._running = True

    def getfilename (self):
        filename = "{:05d}_{}_{}_{}_{}.jpg".format(self.piccount, 
                    time.strftime("%Y%m%d%H%M%S"),
                    control.data[V_GPS_Alt],
                    control.data[V_GPS_Lon],
                    control.data[V_GPS_Lat]).replace("/", "")
        return "{}{}".format(CONFIG.File.picdir, filename)

    def run (self):
        time.sleep(10)
        while self._running:
            if self._takingPictures:
                filename = self.getfilename()
                self.statusled.on()
                Log("taking picture {}".format(filename))
                # subprocess.run(["raspistill", "-w", "3280", "-h", "2464", "-t", "5", "-o", filename])
                subprocess.run(["raspistill", "-w", "1024", "-h", "768", "-t", "5", "-o", filename])
                self.piccount += 1
                self.statusled.off()

                for _ in range(self.intervall*10):
                    if self._running:
                        time.sleep(0.1)
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
        self.__pin = pin
        io.setwarnings(False)
        io.setmode(io.BOARD)
        io.setup(self.__pin, io.OUT)
        self.__last = None
        self.off()

    def io_write (self, status):
        io.output(self.__pin, status)

    def on (self):
        if self.__last != Switch.ON:
            self.io_write(1)
            self.__last = Switch.ON

    def off (self):
        if self.__last != Switch.OFF:
            self.io_write(0)
            self.__last = Switch.OFF

    def flash (self):
        self.on()
        time.sleep(0.05)
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

    def shutdown_message (self):
        self.draw.rectangle((0,0,self.display.width,self.display.height),
                            outline=0, fill=255)
        self.y = self.ypos
        self.draw_line("Shutting down in 5 s ...")
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
        with open(CONFIG.File.csv, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames, delimiter=',')
            writer.writeheader()

    def write (self, data):
        with open(CONFIG.File.csv, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames, delimiter=',')
            writer.writerow(data)


###############################################################################
# Control #####################################################################
class Control (threading.Thread):
    def __init__ (self):
        threading.Thread.__init__(self)
        self.csv       = CSV()
        self.sensors   = Sensors()
        self.statusled = StatusLED(CONFIG.PIN.LED_Status)

        self.data = None
        self.running_on_battery = False
        self._running = True

    def get_gps_data (self):
        return {V_GPS_Time: gps.data_stream.time,
                V_GPS_Lon: gps.data_stream.lon,
                V_GPS_Lat: gps.data_stream.lat,
                V_GPS_Alt: gps.data_stream.alt,
                V_GPS_Climb: gps.data_stream.climb,
                V_GPS_Speed: gps.data_stream.speed,
                V_GPS_Track: gps.data_stream.track,
                V_GPS_ErrLon: gps.data_stream.epx,
                V_GPS_ErrLat: gps.data_stream.epy,
                V_GPS_ErrAlt: gps.data_stream.epv}

    def monitor_battery (self):
        if self.running_on_battery:
            if self.data[V_Voltage] < 6.0:
                Log("Battery low. Shutting down.")
                # A thread cannot be stopped/joined by itself.
                # Therefore shutdown is called in a new thread.
                shutdown_thread = threading.Thread(target=shutdown)
                shutdown_thread.start()
                Log("Shutdown thread started.")

    def run (self):
        while self._running:
            self.data = self.sensors.read()
            self.data[V_RunningOnBattery] = self.running_on_battery
            self.data.update(self.get_gps_data())

            display.print(self.data)
            self.csv.write(self.data)

            self.monitor_battery()

            for _ in range(5):  # sleep for 5 x 2 = 10 seconds
                if not self._running:
                    break

                for i in range(20):  # flash LED every two seconds (heartbeat)
                    if not self._running:
                        break
                    if i == 0:
                        self.statusled.flash()
                    time.sleep(0.1)

        display.off()

    def stop (self):
        self._running = False


###############################################################################
# Flask stuff #################################################################
@app.route('/shutdown')
def API_Shutdown ():
    Log("Shutdown requested")
    shutdown()
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
# Shutdown stuff ##############################################################
def stop_threads ():
    """stops all threads"""
    camera.stop()
    camera.join()
    control.stop()
    control.join()

def shutdown ():
    """shuts down the OS"""
    Log("Shutting down in 5 s ...")
    stop_threads()
    display.shutdown_message()
    time.sleep(5)
    display.off()
    Log("Shutdown now")
    subprocess.run(["sudo", "shutdown", "-h", "now"])

def shutdown_application ():
    """cleanup stuff"""
    Log("Stopping application")
    stop_threads()
    Log("Application stopped")
    sys.exit(0)


###############################################################################
## main #######################################################################
if __name__ == "__main__":
    shutdown_application = Shutdown(shutdown_func=shutdown_application)

    gps = AGPS3mechanism()
    gps.stream_data() 
    gps.run_thread() 

    display = Display()

    control = Control()
    control.start()

    camera = Camera()
    camera.start()

    app.run(host="0.0.0.0", debug=False)

# eof #

