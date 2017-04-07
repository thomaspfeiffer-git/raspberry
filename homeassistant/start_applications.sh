#!/bin/bash
# starts all home automation applications

echo "Starting QueueServer.py ..."
cd Queueserver/
nohup ./QueueServer.py &
echo "QueueServer.py started."
cd ..


echo "Starting Brightness.py ..."
cd Brightness/
nohup ./Brightness.py &
echo "Brightness.py started."
cd ..


echo "Starting Weatherstation.py ..."
cd Weather/
nohup ./Weatherstation.py &
echo "Weatherstation.py started."
cd ..

# eof #

