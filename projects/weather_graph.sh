#/bin/bash

RRDPATH=/schild/
RRD=$RRDPATH/weather.rrd
PNG_TEMP_D=$RRDPATH/weather_temp_d.png
PNG_HUMI_D=$RRDPATH/weather_humi_d.png
PNG_PRES_D=$RRDPATH/weather_pressure_d.png
PNG_CPU_D=$RRDPATH/cpu_temp_d.png
PNG_TEMP_W=$RRDPATH/weather_temp_w.png
PNG_HUMI_W=$RRDPATH/weather_humi_w.png
PNG_PRES_W=$RRDPATH/weather_pressure_w.png
PNG_CPU_W=$RRDPATH/cpu_temp_w.png


WIDTH=1024
HEIGHT=120
WATERMARK=`date  "+%e. %B %Y, %H:%M:%S"`



rrdtool graph $PNG_TEMP_D    \
--title "Temperatur [°C]" \
--end now --start end-36h  \
-w $WIDTH -h $(($HEIGHT*2)) -a PNG       \
--watermark "$WATERMARK" \
--right-axis 1:0         \
DEF:temp_outdoor=$RRD:temp_outdoor:AVERAGE        \
DEF:temp_indoor=$RRD:temp_indoor:AVERAGE          \
LINE1:temp_outdoor#0000FF:"Temperatur außen"    \
GPRINT:temp_outdoor:LAST:"\t Aktuell\: %5.2lf °C" \
GPRINT:temp_outdoor:AVERAGE:"Mittelwert\: %5.2lf °C" \
GPRINT:temp_outdoor:MAX:"Max\: %5.2lf °C" \
GPRINT:temp_outdoor:MIN:"Min\: %5.2lf °C\n"            \
LINE2:temp_indoor#FF0000:"Temperatur innen"      \
GPRINT:temp_indoor:LAST:"\t Aktuell\: %5.2lf °C" \
GPRINT:temp_indoor:AVERAGE:"Mittelwert\: %5.2lf °C" \
GPRINT:temp_indoor:MAX:"Max\: %5.2lf °C" \
GPRINT:temp_indoor:MIN:"Min\: %5.2lf °C\n" \


rrdtool graph $PNG_CPU_D    \
--title "Temperatur Raspberry Pi [°C]" \
--end now --start end-36h  \
-w $WIDTH -h $HEIGHT -a PNG       \
--watermark "$WATERMARK" \
--right-axis 1:0         \
DEF:temp_cpu=$RRD:temp_cpu:AVERAGE                \
LINE1:temp_cpu#FF00FF:"Temperatur Raspberry Pi"      



rrdtool graph $PNG_HUMI_D    \
--title "Luftfeuchtigkeit [%]" \
--end now --start end-36h  \
-w $WIDTH -h $HEIGHT -a PNG       \
--watermark "$WATERMARK" \
--right-axis 1:0                                     \
DEF:humi_outdoor=$RRD:humi_outdoor:AVERAGE           \
DEF:humi_indoor=$RRD:humi_indoor:AVERAGE             \
LINE1:humi_outdoor#0000FF:"Luftfeuchtigkeit außen"   \
GPRINT:humi_outdoor:LAST:"\t Aktuell\: %5.2lf %%" \
GPRINT:humi_outdoor:AVERAGE:"Mittelwert\: %5.2lf %%" \
GPRINT:humi_outdoor:MAX:"Max\: %5.2lf %%" \
GPRINT:humi_outdoor:MIN:"Min\: %5.2lf %%\n"            \
LINE2:humi_indoor#FF0000:"Luftfeuchtigkeit innen"     \
GPRINT:humi_indoor:LAST:"\t Aktuell\: %5.2lf %%" \
GPRINT:humi_indoor:AVERAGE:"Mittelwert\: %5.2lf %%"    \
GPRINT:humi_indoor:MAX:"Max\: %5.2lf %%"               \
GPRINT:humi_indoor:MIN:"Min\: %5.2lf %%\n"            \



rrdtool graph $PNG_PRES_D    \
--title "Luftdruck [hPa]" \
--end now --start end-36h  \
-w $WIDTH -h $HEIGHT -a PNG       \
--alt-autoscale \
--alt-y-grid \
--rigid \
--watermark "$WATERMARK" \
--right-axis 1:0         \
--right-axis-format "%4.0lf" \
DEF:air_pressure=$RRD:air_pressure:AVERAGE        \
LINE1:air_pressure#40FF00:"Luftdruck"             \
GPRINT:air_pressure:LAST:"\t Aktuell\: %5.2lf hPa" \
GPRINT:air_pressure:AVERAGE:"Mittelwert\: %5.2lf hPa" \
GPRINT:air_pressure:MAX:"Max\: %5.2lf hPa" \
GPRINT:air_pressure:MIN:"Min\: %5.2lf hPa\n"            \

#--left-axis-format "%4.0lf" \



rrdtool graph $PNG_TEMP_W    \
--title "Temperatur [°C]" \
--end now --start end-7d  \
-w $WIDTH -h $(($HEIGHT*2)) -a PNG       \
--watermark "$WATERMARK" \
--right-axis 1:0         \
DEF:temp_outdoor=$RRD:temp_outdoor:AVERAGE        \
DEF:temp_indoor=$RRD:temp_indoor:AVERAGE          \
LINE1:temp_outdoor#0000FF:"Temperatur außen"    \
GPRINT:temp_outdoor:LAST:"\t Aktuell\: %5.2lf °C" \
GPRINT:temp_outdoor:AVERAGE:"Mittelwert\: %5.2lf °C" \
GPRINT:temp_outdoor:MAX:"Max\: %5.2lf °C" \
GPRINT:temp_outdoor:MIN:"Min\: %5.2lf °C\n"            \
LINE2:temp_indoor#FF0000:"Temperatur innen"      \
GPRINT:temp_indoor:LAST:"\t Aktuell\: %5.2lf °C" \
GPRINT:temp_indoor:AVERAGE:"Mittelwert\: %5.2lf °C" \
GPRINT:temp_indoor:MAX:"Max\: %5.2lf °C" \
GPRINT:temp_indoor:MIN:"Min\: %5.2lf °C\n" \


rrdtool graph $PNG_CPU_W    \
--title "Temperatur Raspberry Pi [°C]" \
--end now --start end-7d  \
-w $WIDTH -h $HEIGHT -a PNG       \
--watermark "$WATERMARK" \
--right-axis 1:0         \
DEF:temp_cpu=$RRD:temp_cpu:AVERAGE                \
LINE1:temp_cpu#FF00FF:"Temperatur Raspberry Pi"      



rrdtool graph $PNG_HUMI_W    \
--title "Luftfeuchtigkeit [%]" \
--end now --start end-7d  \
-w $WIDTH -h $HEIGHT -a PNG       \
--watermark "$WATERMARK" \
--right-axis 1:0                                     \
DEF:humi_outdoor=$RRD:humi_outdoor:AVERAGE           \
DEF:humi_indoor=$RRD:humi_indoor:AVERAGE             \
LINE1:humi_outdoor#0000FF:"Luftfeuchtigkeit außen"   \
GPRINT:humi_outdoor:LAST:"\t Aktuell\: %5.2lf %%" \
GPRINT:humi_outdoor:AVERAGE:"Mittelwert\: %5.2lf %%" \
GPRINT:humi_outdoor:MAX:"Max\: %5.2lf %%" \
GPRINT:humi_outdoor:MIN:"Min\: %5.2lf %%\n"            \
LINE2:humi_indoor#FF0000:"Luftfeuchtigkeit innen"     \
GPRINT:humi_indoor:LAST:"\t Aktuell\: %5.2lf %%" \
GPRINT:humi_indoor:AVERAGE:"Mittelwert\: %5.2lf %%"    \
GPRINT:humi_indoor:MAX:"Max\: %5.2lf %%"               \
GPRINT:humi_indoor:MIN:"Min\: %5.2lf %%\n"            \



rrdtool graph $PNG_PRES_W    \
--title "Luftdruck [hPa]" \
--end now --start end-7d  \
-w $WIDTH -h $HEIGHT -a PNG       \
--alt-autoscale \
--alt-y-grid \
--rigid \
--watermark "$WATERMARK" \
--right-axis 1:0         \
DEF:air_pressure=$RRD:air_pressure:AVERAGE        \
LINE1:air_pressure#40FF00:"Luftdruck"             \
GPRINT:air_pressure:LAST:"\t Aktuell\: %5.2lf hPa" \
GPRINT:air_pressure:AVERAGE:"Mittelwert\: %5.2lf hPa" \
GPRINT:air_pressure:MAX:"Max\: %5.2lf hPa" \
GPRINT:air_pressure:MIN:"Min\: %5.2lf hPa\n"            \


