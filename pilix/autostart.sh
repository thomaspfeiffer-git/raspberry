#!/bin/bash

# draft of autostart.sh
# shall be called in /etc/rc.local



# switchin wifi on (in case it was turned off)
sudo iwconfig wlan0 txpower auto ; sleep 1 ; sudo iwconfig wlan0 txpower auto


# starting internet access (GSM/GPRS using SIM800L)
sudo pon fona

# starting all pilix stuff
( sleep 60 ; cd /home/pi/raspberry/pilix ; make autostart=autostart ) &


# switching wifi off 3 mins after startup (safe battery)
(sleep 180 ; sudo iwconfig wlan0 txpower off ) &



