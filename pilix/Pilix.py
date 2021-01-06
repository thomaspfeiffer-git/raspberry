#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
###############################################################################
# Pilix.py                                                                    #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2017, 2021             #
###############################################################################
"""Pilix: my Pi in the sky project:
   control weather balloon"""


### usage ###
# nohup ./Pilix.py 2>&1 >./Logs/pilix.log &


### needful things ###
# --- battery control:
#     https://www.raspberrypi.org/forums/viewtopic.php?f=44&t=178015
#
#     /boot/config.txt
#     dtoverlay=gpio-poweroff,active_low,gpiopin=17
#
# --- autostart
#     /etc/rc.local
#     echo ds3231 0x68 > /sys/class/i2c-adapter/i2c-1/new_device
#     sudo hwclock -s
#     cd /home/pi/rasperry/pilix ; ./autostart.sh


# TODO:
# Environment Sensor (BME680, CCS811)


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
#
#
# --- SPI for RFM9x ---
# sudo pip3 install spidev
# raspi-config: enable SPI


import csv
from gps3.agps3threaded import AGPS3mechanism
from enum import Enum
import errno
from flask import Flask, request
import os
import picamera
import RPi.GPIO as io
import subprocess
import sys
import threading
import time

sys.path.append("../libs/")
from Commons import Singleton, Display1306
from Logging import Log
from Shutdown import Shutdown

from sensors.CPU import CPU
from sensors.BMP180 import BMP180
from sensors.DS1820 import DS1820
from sensors.PCF8591 import PCF8591

from config import CONFIG
from csv_fieldnames import *
import Livetracking


app = Flask(__name__)


###############################################################################
# Switch ######################################################################
class Switch (Enum):
    OFF = 0
    ON  = 1


###############################################################################
# Sensors #####################################################################
class Sensors (object):
    v_ref = 8.77

    def __init__ (self):
        self.cpu = CPU()
        self.bmp180 = BMP180()   # air pressure, temperature
        self.ds1820 = DS1820("/sys/bus/w1/devices/28-00000855fdfe/w1_slave")
        self.pcf8591 = PCF8591() # ADC for measurement of supply voltage

    def read (self):
        timestamp = time.time()
        return{V_TemperatureBox: self.bmp180.read_temperature(),
               V_TemperatureOutside: self.ds1820.read_temperature(),
               V_Pressure: self.bmp180.read_pressure(),
               V_Voltage: self.pcf8591.read(channel=0) / 255.0 * self.v_ref,
               V_TemperatureCPU: self.cpu.read_temperature(),
               V_Timestamp: timestamp,
               V_Time: time.strftime("%X", time.localtime(timestamp))}


###############################################################################
# PictureStore ################################################################
class PictureStore (metaclass=Singleton):
    size_of_segment = 100

    def __init__ (self):
        self.picture_count = self.get_next_segment()

    def get_next_segment (self):
        """after restart of the application, we continue on the
           next (empty) directory."""
        from os.path import isdir, join
        dirs = [d for d in os.listdir(CONFIG.File.picdir)
                if isdir(join(CONFIG.File.picdir, d))]
        dirs.sort()
        try:
            return (int(dirs.pop())+1) * self.size_of_segment
        except (IndexError, ValueError):
            return 0

    def get_next_filename (self):
        def get_directory ():
            directory = "{}/{:03d}".format(CONFIG.File.picdir,
                                           self.picture_count//self.size_of_segment)
            try:
                os.makedirs(directory)
            except OSError as exception:
                if exception.errno != errno.EEXIST:
                   raise
            return directory

        filename = "{:05d}_{}_{}_{}_{}.jpg".format(self.picture_count,
                    time.strftime("%Y%m%d%H%M%S"),
                    control.data[V_GPS_Alt],
                    control.data[V_GPS_Lon],
                    control.data[V_GPS_Lat]).replace("/", "")
        self.picture_count += 1
        return "{}/{}".format(get_directory(), filename)


###############################################################################
# Camera ######################################################################
class Camera (threading.Thread):
    intervall = CONFIG.Camera.Intervall

    def __init__ (self):
        threading.Thread.__init__(self)
        self.statusled = StatusLED(CONFIG.PIN.LED_Picture)
        self.picturestore = PictureStore()

        self.camera = picamera.PiCamera()
        self.camera.resolution = (CONFIG.Camera.Width, CONFIG.Camera.Height)
        self.camera.annotate_background = picamera.Color('black')

        # on autostart start taking pictures immediately
        self._takingPictures = CONFIG.APP.autostart
        self._running = True

    def run (self):
        time.sleep(10)

        while self._running:
            if self._takingPictures:
                filename = self.picturestore.get_next_filename()
                self.statusled.on()
                Log("taking picture {}".format(filename))
                self.camera.annotate_text = \
                      "{} - Alt: {} m".format(time.strftime("%Y%m%d %H%M%S"),
                                              control.data[V_GPS_Alt])
                self.camera.capture(filename, quality=CONFIG.Camera.Quality)
                self.statusled.off()

                for _ in range(self.intervall*10):
                    if self._running:
                        time.sleep(0.1)
            else:
                time.sleep(0.1)

    def toggle_takePictures (self):
        self._takingPictures = not self._takingPictures
        Log("Camera: {}".format(self._takingPictures))
        for _ in range(4 if self._takingPictures else 2):
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
        self.last_timestamp_voltage_over_limit = time.time()
        self._running = True

    def get_gps_data (self):
        # d = gps.data_stream.time[:4] != "1970"        # kind of 'n/a'
        d = gps.data_stream.time != "n/a"
        return {V_GPS_Time: gps.data_stream.time,
                V_GPS_Lon: gps.data_stream.lon if d else "n/a",
                V_GPS_Lat: gps.data_stream.lat if d else "n/a",
                V_GPS_Alt: gps.data_stream.alt if d else "n/a",
                V_GPS_Climb: gps.data_stream.climb,
                V_GPS_Speed: gps.data_stream.speed,
                V_GPS_Track: gps.data_stream.track,
                V_GPS_ErrLon: gps.data_stream.epx,
                V_GPS_ErrLat: gps.data_stream.epy,
                V_GPS_ErrAlt: gps.data_stream.epv}

    def monitor_battery (self):
        if self.running_on_battery:
            if self.data[V_Voltage] >= 6.2: # Battery under 6.2 V for more than 60 s.
                self.last_timestamp_voltage_over_limit = time.time()
            if self.last_timestamp_voltage_over_limit + 60 <= time.time():
                Log("Battery low. Shutting down.")
                # A thread cannot be stopped/joined by itself.
                # Therefore shutdown is called in a new thread.
                shutdown_thread = threading.Thread(target=shutdown)
                shutdown_thread.start()
                Log("Shutdown thread started.")
        else:
            self.last_timestamp_voltage_over_limit = time.time()

    def reset_watchdog (self):
        if CONFIG.APP.autostart: # watchdog only in autostart mode
            subprocess.run(["sudo", "bash", "-c", "echo 'hi' > /dev/watchdog"])

    def run (self):
        while self._running:
            self.data = self.sensors.read()
            self.data[V_RunningOnBattery] = self.running_on_battery
            self.data.update(self.get_gps_data())

            display.print(f"Temp: {self.data[V_TemperatureBox]} °C",
                          f"Press: {self.data[V_Pressure] / 100.0} hPa",
                          f"Voltage: {self.data[V_Voltage]:.2f}",
                          f"X: {self.data[V_GPS_Lat]} Y: {self.data[V_GPS_Lon]}",
                          f"Time: {self.data[V_Time]}")
            self.csv.write(self.data)
            livetracking_udp.setdata(self.data)
            livetracking_lora.setdata(self.data)

            self.monitor_battery()

            for _ in range(5):  # sleep for 5 x 2 = 10 seconds
                if not self._running:
                    break

                for i in range(20):  # flash LED every two seconds (heartbeat)
                    if not self._running:
                        break
                    if i == 0:
                        self.statusled.flash()
                        self.reset_watchdog()
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

@app.route('/camera')
def API_ToggleCamera ():
    Log("Camera: toggle requested")
    camera.toggle_takePictures()
    return "camera toggle ok"

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
    livetracking_lora.stop()
    livetracking_lora.join()
    livetracking_udp.stop()
    livetracking_udp.join()
    control.stop()
    control.join()

def shutdown ():
    """shuts down the OS"""
    Log("Shutting down in 5 s ...")
    stop_threads()
    display.print("Shutting down in 5 s ...")
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

    display = Display1306()

    livetracking_udp = Livetracking.Sender_UDP()
    livetracking_udp.start()
    livetracking_lora = Livetracking.Sender_LoRa()
    livetracking_lora.start()

    control = Control()
    control.start()

    camera = Camera()
    camera.start()

    app.run(host="0.0.0.0", debug=False)

# eof #

