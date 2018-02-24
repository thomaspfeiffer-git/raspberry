#!/bin/bash


# Improvements:
# move to python
# done: 1 minute for first 7 days (mind: change cron!)
# done: air pressure: 960..1040

HEARTBEAT=90


rrdtool create /schild/weather.rrd --step 60 \
DS:temp_indoor:GAUGE:$HEARTBEAT:-40:80 \
DS:temp_outdoor:GAUGE:$HEARTBEAT:-40:80 \
DS:humi_indoor:GAUGE:$HEARTBEAT:0:100 \
DS:humi_outdoor:GAUGE:$HEARTBEAT:0:100 \
DS:air_pressure:GAUGE:$HEARTBEAT:960:1040 \
DS:temp_cpu:GAUGE:$HEARTBEAT:-40:80 \
DS:temp_3:GAUGE:$HEARTBEAT:-40:80 \
DS:temp_4:GAUGE:$HEARTBEAT:-40:80 \
RRA:AVERAGE:0.5:1:7200 \
RRA:AVERAGE:0.5:5:4032 \
RRA:AVERAGE:0.5:60:744 \
RRA:AVERAGE:0.5:1440:3650 \


# 7200: 1440 Werte pro Tag x 5 Tage
# 4032: je fünf Werte (= fünf Minuten) = 12 Werte je Stunde = 288 Werte je Tag
#       = 4032 Werte für 14 Tage
# 744:  je 60 Werte (= 1 Stunde) für 31 Tage: = 24*31 = 744 Werte
# 3650: je 1440 Werte (=1 Tag) für 10 Jahre = 3650
