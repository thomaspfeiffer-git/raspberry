#!/bin/bash
# starts all needed applications 


LogDir=./Logs/
PicDir=./Pictures/

if [ ! -d "$LogDir" ]; then
   mkdir "$LogDir"
fi
if [ ! -d "$PicDir" ]; then
   mkdir "$PicDir"
fi


nohup ./Buttons.py > "$LogDir/buttons.log" 2>&1 &
nohup ./Pilix.py > "$LogDir/pilix.log" 2>&1 &

