#!/bin/bash

HEARTBEAT=90


rrdtool create /schild/weather/kitchen.rrd --step 60 \
DS:ki_temp:GAUGE:$HEARTBEAT:-40:80 \
DS:ki_tempcpu:GAUGE:$HEARTBEAT:-40:80 \
DS:ki_humi:GAUGE:$HEARTBEAT:0:100 \
DS:ki_pressure:GAUGE:$HEARTBEAT:960:1040 \
DS:ki_lightness:GAUGE:$HEARTBEAT:0:20000 \
DS:ki_airquality:GAUGE:$HEARTBEAT:0:100 \
DS:ki_temp_1:GAUGE:$HEARTBEAT:-40:80 \
DS:ki_temp_2:GAUGE:$HEARTBEAT:-40:80 \
DS:ki_temp_3:GAUGE:$HEARTBEAT:-40:80 \
DS:ki_temp_4:GAUGE:$HEARTBEAT:-40:80 \
RRA:AVERAGE:0.5:1:7200 \
RRA:AVERAGE:0.5:5:4032 \
RRA:AVERAGE:0.5:60:744 \
RRA:AVERAGE:0.5:1440:3650 \



