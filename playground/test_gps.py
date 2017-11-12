#!/usr/bin/python3
############################################################################
# test_gps.py                                                              #
# (c) Thomas Pfeiffer, 2017                                                #
############################################################################
"""testing adafruit's ultimate GPS
   https://learn.adafruit.com/adafruit-ultimate-gps-on-the-raspberry-pi/introduction
"""

# you might need to install:
# sudo apt-get install gpsd gpsd-clients python-gps -y
# sudo -H pip3 install gps3

# howto start and test:
"""
sudo systemctl stop gpsd.socket
sudo systemctl disable gpsd.socket
sudo gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock

cgps -s
"""

import csv
import sys
import time


from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

sys.path.append('../libs')
from actuators.SSD1306 import SSD1306


disp = SSD1306()
disp.begin()
disp.clear()
disp.display()
xpos = 4
ypos = 4
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()
_, fontheight = font.getsize("A")


from gps3.agps3threaded import AGPS3mechanism
agps_thread = AGPS3mechanism()
agps_thread.stream_data() 
agps_thread.run_thread() 


V_GPS_Time   = "GPS Time"
V_GPS_Lon    = "GPS Longitude"
V_GPS_Lat    = "GPS Latitude"
V_GPS_Alt    = "GPS Altitude"
V_GPS_Climb  = "GPS Climb"
V_GPS_Speed  = "GPS Speed"
V_GPS_Track  = "GPS Track"
V_GPS_ErrLon = "GPS Err Longitude"
V_GPS_ErrLat = "GPS Err Latitude"
V_GPS_ErrAlt = "GPS Err Altitude"

fieldnames = [V_GPS_Time, V_GPS_Lon, V_GPS_Lat, V_GPS_Alt, V_GPS_Climb,
              V_GPS_Speed, V_GPS_Track, V_GPS_ErrLon, V_GPS_ErrLat, V_GPS_ErrAlt]

with open('test_gps.csv', 'a', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',')
    writer.writeheader()


while True:
    # field documentation: http://www.catb.org/gpsd/gpsd_json.html
    gps_data = {V_GPS_Time: agps_thread.data_stream.time,
                V_GPS_Lon: agps_thread.data_stream.lon,
                V_GPS_Lat: agps_thread.data_stream.lat,
                V_GPS_Alt: agps_thread.data_stream.alt,
                V_GPS_Climb: agps_thread.data_stream.climb,
                V_GPS_Speed: agps_thread.data_stream.speed,
                V_GPS_Track: agps_thread.data_stream.track,
                V_GPS_ErrLon: agps_thread.data_stream.epx,
                V_GPS_ErrLat: agps_thread.data_stream.epy,
                V_GPS_ErrAlt: agps_thread.data_stream.epv}
    with open('test_gps.csv', 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',')
        writer.writerow(gps_data)

    draw.rectangle((0,0,width,height), outline=0, fill=255)
    y = ypos
    draw.text((xpos, y), "Lon: {}".format(gps_data[V_GPS_Lon]))
    y += fontheight        
    draw.text((xpos, y), "Lat: {}".format(gps_data[V_GPS_Lat]))
    y += fontheight        
    v = 0 if gps_data[V_GPS_Speed] == "n/a" else gps_data[V_GPS_Speed]
    draw.text((xpos, y), "Speed: {} km/h".format(v*3.6))
    y += fontheight        
    draw.text((xpos, y), "Height: {} m".format(gps_data[V_GPS_Alt]))
    y += fontheight        
    draw.text((xpos, y), "{}".format(gps_data[V_GPS_Time]))
    disp.image(image)
    disp.display()

    time.sleep(10) 

# eof #

