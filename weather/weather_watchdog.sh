#!/bin/bash

PID=weather.py.pid
LOG=weather_watchdog.log

if [ -e $PID ] ; then
  if [ `find $PID -mmin +10` ]; then
    date >> $LOG
    cat $PID >> $LOG
    sudo kill `cat $PID`
    sudo rm $PID
  fi
fi


