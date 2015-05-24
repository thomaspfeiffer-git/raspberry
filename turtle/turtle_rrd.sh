#/bin/bash


HEARTBEAT=90

rrdtool create /schild/weather/turtle.rrd --step 60 \
DS:turtle_temp1:GAUGE:$HEARTBEAT:-40:80 \
DS:turtle_temp2:GAUGE:$HEARTBEAT:-40:80 \
DS:turtle_temp3:GAUGE:$HEARTBEAT:-40:80 \
DS:turtle_tempcpu:GAUGE:$HEARTBEAT:-40:80 \
DS:turtle_humi:GAUGE:$HEARTBEAT:0:100 \
DS:turtle_heating:GAUGE:$HEARTBEAT:0:1 \
RRA:AVERAGE:0.5:1:7200 \
RRA:AVERAGE:0.5:5:4032 \
RRA:AVERAGE:0.5:60:744 \
RRA:AVERAGE:0.5:1440:3650 \


# 7200: 1440 Werte pro Tag x 5 Tage
# 4032: je fünf Werte (= fünf Minuten) = 12 Werte je Stunde = 288 Werte je Tag
#       = 4032 Werte für 14 Tage
# 744:  je 60 Werte (= 1 Stunde) für 31 Tage: = 24*31 = 744 Werte
# 3650: je 1440 Werte (=1 Tag) für 10 Jahre = 3650

