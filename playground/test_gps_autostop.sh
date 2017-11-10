#!/bin/bash

# starts gps monitoring
# can be used in /etc/rc.local at boot time

cd /home/pi/raspberry/playground/


sudo systemctl stop gpsd.socket
sudo systemctl disable gpsd.socket
sudo gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock


sleep 10


./test_gps.py



