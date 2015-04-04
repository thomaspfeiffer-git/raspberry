#/bin/bash


# Improvements:
# move to python
# 1 minute for first 7 days (mind: change cron!)
# air pressure: 960..1040

HEARTBEAT=650


rrdtool create /schild/weather.rrd --step 300 \
DS:temp_indoor:GAUGE:$HEARTBEAT:-40:80 \
DS:temp_outdoor:GAUGE:$HEARTBEAT:-40:80 \
DS:humi_indoor:GAUGE:$HEARTBEAT:0:100 \
DS:humi_outdoor:GAUGE:$HEARTBEAT:0:100 \
DS:air_pressure:GAUGE:$HEARTBEAT:900:1100 \
DS:temp_cpu:GAUGE:$HEARTBEAT:-40:80 \
DS:temp_3:GAUGE:$HEARTBEAT:-40:80 \
DS:temp_4:GAUGE:$HEARTBEAT:-40:80 \
RRA:AVERAGE:0.5:1:288 \
RRA:AVERAGE:0.5:6:480 \
RRA:AVERAGE:0.5:12:480 \
RRA:AVERAGE:0.5:24:480 \
RRA:AVERAGE:0.5:288:3650 \


