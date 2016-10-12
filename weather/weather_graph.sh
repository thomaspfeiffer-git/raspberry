#/bin/bash

RRDPATH=/schild/weather/
RRD=$RRDPATH/weather.rrd
RRD_K=$RRDPATH/weather_kidsroom.rrd
RRD_KB=$RRDPATH/weather_kollerberg.rrd


PNG_TEMP_D=$RRDPATH/weather_temp_d.png
PNG_TEMP_W=$RRDPATH/weather_temp_w.png
PNG_TEMP_M=$RRDPATH/weather_temp_m.png
PNG_TEMP_Y=$RRDPATH/weather_temp_y.png

PNG_HUMI_D=$RRDPATH/weather_humi_d.png
PNG_HUMI_W=$RRDPATH/weather_humi_w.png
PNG_HUMI_M=$RRDPATH/weather_humi_m.png
PNG_HUMI_Y=$RRDPATH/weather_humi_y.png

PNG_PRES_D=$RRDPATH/weather_pressure_d.png
PNG_PRES_W=$RRDPATH/weather_pressure_w.png
PNG_PRES_M=$RRDPATH/weather_pressure_m.png
PNG_PRES_Y=$RRDPATH/weather_pressure_y.png

PNG_CPU_D=$RRDPATH/cpu_temp_d.png
PNG_CPU_W=$RRDPATH/cpu_temp_w.png
PNG_CPU_M=$RRDPATH/cpu_temp_m.png
PNG_CPU_Y=$RRDPATH/cpu_temp_y.png

PNG_HEATING_D=$RRDPATH/heating_d.png
PNG_HEATING_W=$RRDPATH/heating_w.png
PNG_HEATING_M=$RRDPATH/heating_m.png
PNG_HEATING_Y=$RRDPATH/heating_y.png



WIDTH=1024
HEIGHT=160
WATERMARK=`date  "+%e. %B %Y, %H:%M:%S"`




#######################################################################
# Parameter:                                                          #
# $1 Time Range                                                       #
# $2 Filename                                                         #
#######################################################################
printTemp ()
  {
    rrdtool graph $2                                         \
    --title "Temperatur [°C]"                                \
    --end now --start end-$1                                 \
    -w $WIDTH -h $(($HEIGHT*2)) -a PNG                       \
    --watermark "$WATERMARK"                                 \
    --right-axis 1:0                                         \
    DEF:temp_outdoor=$RRD:temp_outdoor:AVERAGE               \
    DEF:temp_realoutdoor=$RRD:temp_3:AVERAGE                 \
    DEF:temp_indoor=$RRD:temp_indoor:AVERAGE                 \
    DEF:temp_window=$RRD:temp_4:AVERAGE                      \
    DEF:kidsroom_temp1=$RRD_K:kidsroom_temp1:AVERAGE         \
    DEF:kb_i_t1=$RRD_KB:kb_i_t1:AVERAGE                      \
    DEF:kb_a_t1=$RRD_KB:kb_a_t1:AVERAGE                      \
    DEF:kb_k_t1=$RRD_KB:kb_k_t1:AVERAGE                      \
    LINE1:temp_outdoor#0000FF:"Temperatur Wien außen         "   \
    GPRINT:temp_outdoor:LAST:"Aktuell\: %5.2lf °C"           \
    GPRINT:temp_outdoor:AVERAGE:"Mittelwert\: %5.2lf °C"     \
    GPRINT:temp_outdoor:MAX:"Max\: %5.2lf °C"                \
    GPRINT:temp_outdoor:MIN:"Min\: %5.2lf °C\n"              \
    LINE1:temp_realoutdoor#666633:"Temperatur Wien ganz außen    " \
    GPRINT:temp_realoutdoor:LAST:"Aktuell\: %5.2lf °C"       \
    GPRINT:temp_realoutdoor:AVERAGE:"Mittelwert\: %5.2lf °C" \
    GPRINT:temp_realoutdoor:MAX:"Max\: %5.2lf °C"            \
    GPRINT:temp_realoutdoor:MIN:"Min\: %5.2lf °C\n"          \
    LINE1:temp_indoor#FF0000:"Temperatur Wohnzimmer         "    \
    GPRINT:temp_indoor:LAST:"Aktuell\: %5.2lf °C"            \
    GPRINT:temp_indoor:AVERAGE:"Mittelwert\: %5.2lf °C"      \
    GPRINT:temp_indoor:MAX:"Max\: %5.2lf °C"                 \
    GPRINT:temp_indoor:MIN:"Min\: %5.2lf °C\n"               \
    LINE1:temp_window#ff80ff:"Temperatur Fensterbrett       "    \
    GPRINT:temp_window:LAST:"Aktuell\: %5.2lf °C"            \
    GPRINT:temp_window:AVERAGE:"Mittelwert\: %5.2lf °C"      \
    GPRINT:temp_window:MAX:"Max\: %5.2lf °C"                 \
    GPRINT:temp_window:MIN:"Min\: %5.2lf °C\n"               \
    LINE1:kidsroom_temp1#00ccff:"Temperatur Kinderzimmer       " \
    GPRINT:kidsroom_temp1:LAST:"Aktuell\: %5.2lf °C"         \
    GPRINT:kidsroom_temp1:AVERAGE:"Mittelwert\: %5.2lf °C"   \
    GPRINT:kidsroom_temp1:MAX:"Max\: %5.2lf °C"              \
    GPRINT:kidsroom_temp1:MIN:"Min\: %5.2lf °C\n"            \
    LINE1:kb_i_t1#40FF00:"Temperatur Kollerberg innen   "    \
    GPRINT:kb_i_t1:LAST:"Aktuell\: %5.2lf °C"                \
    GPRINT:kb_i_t1:AVERAGE:"Mittelwert\: %5.2lf °C"          \
    GPRINT:kb_i_t1:MAX:"Max\: %5.2lf °C"                     \
    GPRINT:kb_i_t1:MIN:"Min\: %5.2lf °C\n"                   \
    LINE1:kb_a_t1#009900:"Temperatur Kollerberg außen   "    \
    GPRINT:kb_a_t1:LAST:"Aktuell\: %5.2lf °C"                \
    GPRINT:kb_a_t1:AVERAGE:"Mittelwert\: %5.2lf °C"          \
    GPRINT:kb_a_t1:MAX:"Max\: %5.2lf °C"                     \
    GPRINT:kb_a_t1:MIN:"Min\: %5.2lf °C\n"                   \
    LINE1:kb_k_t1#663300:"Temperatur Kollerberg Keller  "    \
    GPRINT:kb_k_t1:LAST:"Aktuell\: %5.2lf °C"                \
    GPRINT:kb_k_t1:AVERAGE:"Mittelwert\: %5.2lf °C"          \
    GPRINT:kb_k_t1:MAX:"Max\: %5.2lf °C"                     \
    GPRINT:kb_k_t1:MIN:"Min\: %5.2lf °C\n"
 }


#######################################################################
# printCPUTemp()                                                      #
# Parameter:                                                          #
# $1 Time Range                                                       #
# $2 Filename                                                         #
#######################################################################
printCPUTemp ()
  {
    rrdtool graph $2                                                     \
    --title "Temperatur Raspberry Pi [°C]"                               \
    --end now --start end-$1                                             \
    -w $WIDTH -h $HEIGHT -a PNG                                          \
    --watermark "$WATERMARK"                                             \
    --right-axis 1:0                                                     \
    DEF:temp_cpu=$RRD:temp_cpu:AVERAGE                                   \
    DEF:kidsroom_tempcpu=$RRD_K:kidsroom_tempcpu:AVERAGE                 \
    DEF:kb_i_tcpu=$RRD_KB:kb_i_tcpu:AVERAGE                              \
    DEF:kb_a_tcpu=$RRD_KB:kb_a_tcpu:AVERAGE                              \
    DEF:kb_k_tcpu=$RRD_KB:kb_k_tcpu:AVERAGE                              \
    LINE1:temp_cpu#FF0000:"Temperatur Raspberry Pi Wohnzimmer       "    \
    GPRINT:temp_cpu:LAST:"\t Aktuell\: %5.2lf °C"                        \
    GPRINT:temp_cpu:AVERAGE:"Mittelwert\: %5.2lf °C"                     \
    GPRINT:temp_cpu:MAX:"Max\: %5.2lf °C"                                \
    GPRINT:temp_cpu:MIN:"Min\: %5.2lf °C\n"                              \
    LINE1:kidsroom_tempcpu#00ccff:"Temperatur Raspberry Pi Kinderzimmer     " \
    GPRINT:kidsroom_tempcpu:LAST:"\t Aktuell\: %5.2lf °C"                \
    GPRINT:kidsroom_tempcpu:AVERAGE:"Mittelwert\: %5.2lf °C"             \
    GPRINT:kidsroom_tempcpu:MAX:"Max\: %5.2lf °C"                        \
    GPRINT:kidsroom_tempcpu:MIN:"Min\: %5.2lf °C\n"                      \
    LINE1:kb_i_tcpu#40FF00:"Temperatur Raspberry Pi Kollerberg innen "   \
    GPRINT:kb_i_tcpu:LAST:"\t Aktuell\: %5.2lf °C"                       \
    GPRINT:kb_i_tcpu:AVERAGE:"Mittelwert\: %5.2lf °C"                    \
    GPRINT:kb_i_tcpu:MAX:"Max\: %5.2lf °C"                               \
    GPRINT:kb_i_tcpu:MIN:"Min\: %5.2lf °C\n"                             \
    LINE1:kb_a_tcpu#009900:"Temperatur Raspberry Pi Kollerberg außen "   \
    GPRINT:kb_a_tcpu:LAST:"\t Aktuell\: %5.2lf °C"                       \
    GPRINT:kb_a_tcpu:AVERAGE:"Mittelwert\: %5.2lf °C"                    \
    GPRINT:kb_a_tcpu:MAX:"Max\: %5.2lf °C"                               \
    GPRINT:kb_a_tcpu:MIN:"Min\: %5.2lf °C\n"                             \
    LINE1:kb_k_tcpu#663300:"Temperatur Raspberry Pi Kollerberg Keller"   \
    GPRINT:kb_k_tcpu:LAST:"\t Aktuell\: %5.2lf °C"                       \
    GPRINT:kb_k_tcpu:AVERAGE:"Mittelwert\: %5.2lf °C"                    \
    GPRINT:kb_k_tcpu:MAX:"Max\: %5.2lf °C"                               \
    GPRINT:kb_k_tcpu:MIN:"Min\: %5.2lf °C\n" 
 }



#######################################################################
# printHumidity()                                                     #
# Parameter:                                                          #
# $1 Time Range                                                       #
# $2 Filename                                                         #
#######################################################################
printHumidity ()
  {
    rrdtool graph $2                                           \
    --title "Luftfeuchtigkeit [%]"                             \
    --end now --start end-$1                                   \
    -w $WIDTH -h $HEIGHT -a PNG                                \
    --watermark "$WATERMARK"                                   \
    --right-axis 1:0                                           \
    DEF:humi_outdoor=$RRD:humi_outdoor:AVERAGE                 \
    DEF:humi_indoor=$RRD:humi_indoor:AVERAGE                   \
    DEF:kidsroom_humi=$RRD_K:kidsroom_humi:AVERAGE             \
    DEF:kb_i_humi=$RRD_KB:kb_i_humi:AVERAGE                    \
    DEF:kb_a_humi=$RRD_KB:kb_a_humi:AVERAGE                    \
    DEF:kb_k_humi=$RRD_KB:kb_k_humi:AVERAGE                    \
    LINE1:humi_outdoor#0000FF:"Luftfeuchtigkeit Wien außen       "  \
    GPRINT:humi_outdoor:LAST:"\t Aktuell\: %5.2lf %%"          \
    GPRINT:humi_outdoor:AVERAGE:"Mittelwert\: %5.2lf %%"       \
    GPRINT:humi_outdoor:MAX:"Max\: %5.2lf %%"                  \
    GPRINT:humi_outdoor:MIN:"Min\: %5.2lf %%\n"                \
    LINE1:humi_indoor#FF0000:"Luftfeuchtigkeit Wohnzimmer       "   \
    GPRINT:humi_indoor:LAST:"\t Aktuell\: %5.2lf %%"           \
    GPRINT:humi_indoor:AVERAGE:"Mittelwert\: %5.2lf %%"        \
    GPRINT:humi_indoor:MAX:"Max\: %5.2lf %%"                   \
    GPRINT:humi_indoor:MIN:"Min\: %5.2lf %%\n"                 \
    LINE1:kidsroom_humi#00ccff:"Luftfeuchtigkeit Kinderzimmer     " \
    GPRINT:kidsroom_humi:LAST:"\t Aktuell\: %5.2lf %%"         \
    GPRINT:kidsroom_humi:AVERAGE:"Mittelwert\: %5.2lf %%"      \
    GPRINT:kidsroom_humi:MAX:"Max\: %5.2lf %%"                 \
    GPRINT:kidsroom_humi:MIN:"Min\: %5.2lf %%\n"               \
    LINE1:kb_i_humi#40FF00:"Luftfeuchtigkeit Kollerberg innen " \
    GPRINT:kb_i_humi:LAST:"\t Aktuell\: %5.2lf %%"             \
    GPRINT:kb_i_humi:AVERAGE:"Mittelwert\: %5.2lf %%"          \
    GPRINT:kb_i_humi:MAX:"Max\: %5.2lf %%"                     \
    GPRINT:kb_i_humi:MIN:"Min\: %5.2lf %%\n"                   \
    LINE1:kb_a_humi#009900:"Luftfeuchtigkeit Kollerberg außen " \
    GPRINT:kb_a_humi:LAST:"\t Aktuell\: %5.2lf %%"             \
    GPRINT:kb_a_humi:AVERAGE:"Mittelwert\: %5.2lf %%"          \
    GPRINT:kb_a_humi:MAX:"Max\: %5.2lf %%"                     \
    GPRINT:kb_a_humi:MIN:"Min\: %5.2lf %%\n"                   \
    LINE1:kb_k_humi#663300:"Luftfeuchtigkeit Kollerberg Keller" \
    GPRINT:kb_k_humi:LAST:"\t Aktuell\: %5.2lf %%"             \
    GPRINT:kb_k_humi:AVERAGE:"Mittelwert\: %5.2lf %%"          \
    GPRINT:kb_k_humi:MAX:"Max\: %5.2lf %%"                     \
    GPRINT:kb_k_humi:MIN:"Min\: %5.2lf %%\n"
 }


#######################################################################
# printAirPressure()                                                  #
# Parameter:                                                          #
# $1 Time Range                                                       #
# $2 Filename                                                         #
#######################################################################
printAirPressure ()
  {
    rrdtool graph $2                                     \
    --title "Luftdruck [hPa]"                            \
    --end now --start end-$1                             \
    -w $WIDTH -h $HEIGHT -a PNG                          \
    --alt-autoscale                                      \
    --alt-y-grid                                         \
    --rigid                                              \
    --watermark "$WATERMARK"                             \
    --right-axis 1:0                                     \
    --right-axis-format "%4.0lf"                         \
    DEF:air_pressure=$RRD:air_pressure:AVERAGE           \
    DEF:kb_i_press=$RRD_KB:kb_i_press:AVERAGE            \
    LINE1:air_pressure#0000FF:"Luftdruck Wien       "    \
    GPRINT:air_pressure:LAST:"\t Aktuell\: %5.2lf hPa"   \
    GPRINT:air_pressure:AVERAGE:"Mittelwert\: %5.2lf hPa" \
    GPRINT:air_pressure:MAX:"Max\: %5.2lf hPa"           \
    GPRINT:air_pressure:MIN:"Min\: %5.2lf hPa\n"         \
    LINE1:kb_i_press#40FF00:"Luftdruck Kollerberg "      \
    GPRINT:kb_i_press:LAST:"\t Aktuell\: %5.2lf hPa"     \
    GPRINT:kb_i_press:AVERAGE:"Mittelwert\: %5.2lf hPa"  \
    GPRINT:kb_i_press:MAX:"Max\: %5.2lf hPa"             \
    GPRINT:kb_i_press:MIN:"Min\: %5.2lf hPa\n"
 }



printTemp "36h", "$PNG_TEMP_D"
printTemp "7d",  "$PNG_TEMP_W"
printTemp "30d", "$PNG_TEMP_M"
printTemp "365d", "$PNG_TEMP_Y"

printCPUTemp "36h", "$PNG_CPU_D"
printCPUTemp "7d",  "$PNG_CPU_W"
printCPUTemp "30d", "$PNG_CPU_M"
printCPUTemp "365d", "$PNG_CPU_Y"

printHumidity "36h", "$PNG_HUMI_D"
printHumidity "7d",  "$PNG_HUMI_W"
printHumidity "30d", "$PNG_HUMI_M"
printHumidity "365d", "$PNG_HUMI_Y"

printAirPressure "36h", "$PNG_PRES_D"
printAirPressure "7d",  "$PNG_PRES_W"
printAirPressure "30d", "$PNG_PRES_M"
printAirPressure "365d", "$PNG_PRES_Y"


