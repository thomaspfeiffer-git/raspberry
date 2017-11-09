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

import pprint

from gps3 import gps3
gps_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()
gps_socket.connect()
gps_socket.watch()


for new_data in gps_socket:
    if new_data:
        data_stream.unpack(new_data)
 
        print('Time:      ', data_stream.TPV['time'])
        print('Longitude: ', data_stream.TPV['lon'])
        print('Latitude:  ', data_stream.TPV['lat'])
        print('Altitude:  ', data_stream.TPV['alt'])
        print('Climb:     ', data_stream.TPV['climb'])
        print('Speed:     ', data_stream.TPV['speed'])
        print("Track:     ", data_stream.TPV['track'])
        print("Long Err:  ", data_stream.TPV['epx'])
        print("Lat Err:   ", data_stream.TPV['epy'])
        print("Alt Err:   ", data_stream.TPV['epv'])
        print("")

# eof #

