#!/bin/bash

# starts gps monitoring
# can be used in /etc/rc.local at boot time

cd /home/pi/raspberry/playground/gps/


sleep 10

sudo systemctl stop gpsd.socket  >> /home/pi/rclocal.log
sudo systemctl disable gpsd.socket >> /home/pi/rclocal.log
sudo gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock  >> /home/pi/rclocal.log


sleep 10

# shutdown after amount of time in order to save battery
if [ "$1" == "autostop" ] ; then
   echo "starting test_gps" >> rclocal.log
   ./test_gps.py >> rclocal.log & sleep 3600 ; echo "stopping" ;  sudo shutdown -h now
   exit
fi

./test_gps.py



