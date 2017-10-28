#!/bin/bash
# starts all needed applications for control of lightness of anteroom

cd /home/pi/raspberry/anteroom/

./Anteroom.py >  anteroom_autostart.log 2>&1 &
                                              
sleep 5
                                              
./Relais.py > relais_autostart.log 2>&1 &     
./Button.py > button_autostart.log 2>&1 &     

# eof #

