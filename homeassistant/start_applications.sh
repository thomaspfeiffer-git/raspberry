#!/bin/bash
# starts all home automation applications



(
echo "Starting Watchdog.py ..."
cd ../watchdog/
sudo ./Watchdog.py --receiver  2>&1 > watchdog.log &
echo "Watchdog.py started."
)


echo "Starting Openweather.py ..."
cd Openweather/
nohup ./Openweather.py  2>&1 >openweather.log &
echo "Openweather.py started."
cd ..


echo "Starting Receive_UDP_Data.py ..."
cd UDP/
nohup ./Receive_UDP_Data.py 2>receive_udp_data.log 1>/dev/null &
echo "Receive_UDP_Data.py started."
cd ..


echo "Starting QueueServer.py ..."
cd Queueserver/
nohup ./QueueServer.py &
echo "QueueServer.py started."
cd ..


echo "Starting Sensors.py ..."
cd Sensors/
nohup ./Sensors.py 2>&1 > sensors.log &
echo "Sensors.py started."
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
nohup ./Weatherstation.py 2>&1 > weatherstation.log &
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
echo "Starting other controls ('OtherControls')"
cd OtherControls
nohup ./OtherControls.py &
echo "OtherControls started"
cd ..


echo
echo "Starting Awattar"
cd Awattar
nohup ./Awattar.py 2>&1 > awattar.log &
echo "Awattar started"
cd ..


echo
echo "Starting Radio.py (after sleep)"
cd Radio
( sleep 5 ; nohup ./Radio.py 2>&1 > radio.log & ) &
echo "Radio.py started"
cd ..





# eof #

