#!/bin/bash
# starts all needed applications 

LogDir=./Logs/
PicDir=./Pictures/


# starting GPS stuff
sudo systemctl stop gpsd.socket
sudo systemctl disable gpsd.socket
sudo gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock


if [ ! -d "$LogDir" ]; then
   mkdir "$LogDir"
fi
if [ ! -d "$PicDir" ]; then
   mkdir "$PicDir"
fi


nohup ./Buttons.py >> "$LogDir/buttons.log" 2>>"$LogDir/buttons.err" &
nohup ./Pilix.py >> "$LogDir/pilix.log" 2>>"$LogDir/pilix.err" &

