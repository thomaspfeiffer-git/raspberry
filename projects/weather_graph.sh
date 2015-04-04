#/bin/bash

RRDPATH=/schild/
RRD=$RRDPATH/weather.rrd
PNG_TEMP=$RRDPATH/weather_temp.png
PNG_HUMI=$RRDPATH/weather_humi.png
PNG_PRES=$RRDPATH/weather_pressure.png
PNG_CPU=$RRDPATH/cpu_temp.png

WIDTH=1024
HEIGHT=120
WATERMARK=`date  "+%e. %B %Y, %H:%M:%S"`

rrdtool graph $PNG_TEMP    \
--title "Temperatur [°C]" \
--end now --start end-12h  \
-w $WIDTH -h $(($HEIGHT*2)) -a PNG       \
--watermark "$WATERMARK" \
--right-axis 1:0         \
DEF:temp_outdoor=$RRD:temp_outdoor:AVERAGE        \
LINE1:temp_outdoor#0000FF:"Temperatur outdoor"    \
DEF:temp_indoor=$RRD:temp_indoor:AVERAGE          \
LINE2:temp_indoor#FF0000:"Temperatur indoor"      \

rrdtool graph $PNG_CPU    \
--title "Temperatur Raspberry Pi [°C]" \
--end now --start end-12h  \
-w $WIDTH -h $HEIGHT -a PNG       \
--watermark "$WATERMARK" \
--right-axis 1:0         \
DEF:temp_cpu=$RRD:temp_cpu:AVERAGE                \
LINE1:temp_cpu#FF00FF:"Temperatur Raspberry Pi [°C]"      

rrdtool graph $PNG_HUMI    \
--title "Luftfeuchtigkeit [%]" \
--end now --start end-12h  \
-w $WIDTH -h $HEIGHT -a PNG       \
--watermark "$WATERMARK" \
--right-axis 1:0                                     \
DEF:humi_outdoor=$RRD:humi_outdoor:AVERAGE           \
LINE1:humi_outdoor#0000FF:"Luftfeuchtigkeit outdoor" \
DEF:humi_indoor=$RRD:humi_indoor:AVERAGE             \
LINE2:humi_indoor#FF0000:"Luftfeuchtigkeit indoor" 

rrdtool graph $PNG_PRES    \
--title "Luftdruck [hPas]" \
--end now --start end-12h  \
-w $WIDTH -h $HEIGHT -a PNG       \
--alt-autoscale \
--alt-y-grid \
--rigid \
--watermark "$WATERMARK" \
--right-axis 1:0         \
DEF:air_pressure=$RRD:air_pressure:AVERAGE        \
LINE1:air_pressure#40FF00:"Luftdruck [hPas]"  

