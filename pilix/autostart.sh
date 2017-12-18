#!/bin/bash

# draft of autostart.sh
# shall be called in /etc/rc.local


# switching wifi off 3 mins after startup (safe battery)
# starting internet access (GSM/GPRS using SIM800L)
(sleep 60 ; sudo ifconfig wlan0 down ; sleep 10 ; sudo pon fona ) &

# starting all pilix stuff
( sleep 120 ; cd /home/pi/raspberry/pilix ; make autostart=autostart ) &





