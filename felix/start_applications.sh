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


nohup sudo ./Buttons.py > "$LogDir/buttons.log" 2>&1 &
nohup ./Felix.py > "$LogDir/felix.log" 2>&1 &

