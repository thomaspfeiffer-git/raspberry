#/bin/bash

RRDPATH=/schild/
RRD=$RRDPATH/weather.rrd
PNG_TEMP=$RRDPATH/weather_temp.png
PNG_HUMI=$RRDPATH/weather_humi.png
PNG_PRES=$RRDPATH/weather_pressure.png
PNG_CPU=$RRDPATH/cpu_temp.png

rrdtool graph $PNG_TEMP    \
--end now --start end-12h  \
-w 785 -h 120 -a PNG       \
DEF:temp_outdoor=$RRD:temp_outdoor:AVERAGE        \
LINE1:temp_outdoor#0000FF:"temp_outdoor"          \
DEF:temp_indoor=$RRD:temp_indoor:AVERAGE          \
LINE2:temp_indoor#FF0000:"temp_indoor"            \

rrdtool graph $PNG_CPU    \
--end now --start end-12h  \
-w 785 -h 120 -a PNG       \
DEF:temp_cpu=$RRD:temp_cpu:AVERAGE                \
LINE1:temp_cpu#FF00FF:"temp_cpu"                  \

rrdtool graph $PNG_HUMI    \
--end now --start end-12h  \
-w 785 -h 120 -a PNG       \
DEF:humi_outdoor=$RRD:humi_outdoor:AVERAGE        \
LINE1:humi_outdoor#0000FF:"humi_outdoor"          \
DEF:humi_indoor=$RRD:humi_indoor:AVERAGE          \
LINE2:humi_indoor#FF0000:"humi_indoor"            \

rrdtool graph $PNG_PRES    \
--end now --start end-12h  \
-w 785 -h 120 -a PNG       \
--upper-limit 1020 --lower-limit 980  --rigid     \
DEF:air_pressure=$RRD:air_pressure:AVERAGE        \
LINE1:air_pressure#40FF00:"air_pressure"          \

