#!/bin/bash
# starts all home automation applications

echo "Starting QueueServer.py ..."
cd Queueserver/
nohup ./QueueServer.py &
echo "QueueServer.py started."
cd ..


echo
echo "Starting Brightness.py ..."
cd Brightness/
nohup ./Brightness.py &
echo "Brightness.py started."
cd ..

echo
echo "Starting Weatherstation.py ..."
cd Weatherstation/
nohup ./Weatherstation.py &
echo "Weatherstation.py started."
cd ..


echo
echo "Starting Timer.py ..."
cd Timer/
nohup ./Timer.py &
echo "Timer.py started."
cd ..


echo
echo "Starting Message of the Day ..."
cd MessageOfTheDay
nohup ./MessageOfTheDay.py &
echo "Message of the Day started."
cd ..


echo
echo "Starting anteroom lighting control"
cd Anteroom
nohup ./Anteroom.py &
echo "Anteroom lighting control started"
cd ..



# eof #

