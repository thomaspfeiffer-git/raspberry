#/bin/bash

echo -n `date`
echo -n ": rrdtool processes running: "
ps aux | grep "rrdtool" | wc -l

if [ $(ps aux | grep "rrdtool" | wc -l) -gt 1 ] ; then
    echo -n `date`
    echo "rrdtool already running, killing"
    killall rrdtool
    echo ""
    exit 1
fi


RRDPATH=/home/thomas/rrd/
RRD=$RRDPATH/databases/seti.rrd
PICS=$RRDPATH/temp/
PICS_STORE=$RRDPATH/graphs/

WIDTH=1024
HEIGHT=160
WATERMARK=`date  "+%e. %B %Y, %H:%M:%S"`

PNG_LOAD_D=$PICS/seti_load_d.png
PNG_LOAD_W=$PICS/seti_load_w.png
PNG_LOAD_M=$PICS/seti_load_m.png
PNG_LOAD_Y=$PICS/seti_load_y.png

PNG_FREQ_D=$PICS/seti_freq_d.png
PNG_FREQ_W=$PICS/seti_freq_w.png
PNG_FREQ_M=$PICS/seti_freq_m.png
PNG_FREQ_Y=$PICS/seti_freq_y.png

PNG_TEMP_D=$PICS/seti_temp_d.png
PNG_TEMP_W=$PICS/seti_temp_w.png
PNG_TEMP_M=$PICS/seti_temp_m.png
PNG_TEMP_Y=$PICS/seti_temp_y.png

PNG_HUMIDITY_D=$PICS/seti_humidity_d.png
PNG_HUMIDITY_W=$PICS/seti_humidity_w.png
PNG_HUMIDITY_M=$PICS/seti_humidity_m.png
PNG_HUMIDITY_Y=$PICS/seti_humidity_y.png


#######################################################################
# Parameter:                                                          #
# $1 Time Range                                                       #
# $2 Filename                                                         #
#######################################################################
printLoad ()
  {
    rrdtool graph $2                                         \
    --title "Load"                                           \
    --end now --start end-$1                                 \
    -w $WIDTH -h $(($HEIGHT*2)) -a PNG                       \
    --watermark "$WATERMARK"                                 \
    --right-axis 1:0                                         \
    DEF:1_load=$RRD:1_load:AVERAGE                           \
    DEF:2_load=$RRD:2_load:AVERAGE                           \
    DEF:3_load=$RRD:3_load:AVERAGE                           \
    DEF:4_load=$RRD:4_load:AVERAGE                           \
    LINE1:1_load#0000FF:"Load seti_01         "              \
    GPRINT:1_load:LAST:"Aktuell\: %5.2lf"                    \
    GPRINT:1_load:AVERAGE:"Mittelwert\: %5.2lf"              \
    GPRINT:1_load:MAX:"Max\: %5.2lf"                         \
    GPRINT:1_load:MIN:"Min\: %5.2lf\n"                       \
    LINE1:2_load#00FF00:"Load seti_02         "              \
    GPRINT:2_load:LAST:"Aktuell\: %5.2lf"                    \
    GPRINT:2_load:AVERAGE:"Mittelwert\: %5.2lf"              \
    GPRINT:2_load:MAX:"Max\: %5.2lf"                         \
    GPRINT:2_load:MIN:"Min\: %5.2lf\n"                       \
    LINE1:3_load#FF0000:"Load seti_03         "              \
    GPRINT:3_load:LAST:"Aktuell\: %5.2lf"                    \
    GPRINT:3_load:AVERAGE:"Mittelwert\: %5.2lf"              \
    GPRINT:3_load:MAX:"Max\: %5.2lf"                         \
    GPRINT:3_load:MIN:"Min\: %5.2lf\n"                       \
    LINE1:4_load#FFFF00:"Load seti_04         "              \
    GPRINT:4_load:LAST:"Aktuell\: %5.2lf"                    \
    GPRINT:4_load:AVERAGE:"Mittelwert\: %5.2lf"              \
    GPRINT:4_load:MAX:"Max\: %5.2lf"                         \
    GPRINT:4_load:MIN:"Min\: %5.2lf\n"
 }


#######################################################################
# Parameter:                                                          #
# $1 Time Range                                                       #
# $2 Filename                                                         #
#######################################################################
printFreq ()
  {
    rrdtool graph $2                                         \
    --title "Frequenz [MHz]"                                 \
    --end now --start end-$1                                 \
    -w $WIDTH -h $HEIGHT -a PNG                              \
    --watermark "$WATERMARK"                                 \
    --right-axis 1:0                                         \
    DEF:1_freq=$RRD:1_freq:AVERAGE                           \
    DEF:2_freq=$RRD:2_freq:AVERAGE                           \
    DEF:3_freq=$RRD:3_freq:AVERAGE                           \
    DEF:4_freq=$RRD:4_freq:AVERAGE                           \
    LINE1:1_freq#0000FF:"Frequenz seti_01                "   \
    GPRINT:1_freq:LAST:"Aktuell\: %5.2lf MHz"                \
    GPRINT:1_freq:AVERAGE:"Mittelwert\: %5.2lf MHz"          \
    GPRINT:1_freq:MAX:"Max\: %5.2lf MHz"                     \
    GPRINT:1_freq:MIN:"Min\: %5.2lf MHz\n"                   \
    LINE1:2_freq#00FF00:"Frequenz seti_02                "   \
    GPRINT:2_freq:LAST:"Aktuell\: %5.2lf MHz"                \
    GPRINT:2_freq:AVERAGE:"Mittelwert\: %5.2lf MHz"          \
    GPRINT:2_freq:MAX:"Max\: %5.2lf MHz"                     \
    GPRINT:2_freq:MIN:"Min\: %5.2lf MHz\n"                   \
    LINE1:3_freq#FF0000:"Frequenz seti_03                "   \
    GPRINT:3_freq:LAST:"Aktuell\: %5.2lf MHz"                \
    GPRINT:3_freq:AVERAGE:"Mittelwert\: %5.2lf MHz"          \
    GPRINT:3_freq:MAX:"Max\: %5.2lf MHz"                     \
    GPRINT:3_freq:MIN:"Min\: %5.2lf MHz\n"                   \
    LINE1:4_freq#FFFF00:"Frequenz seti_04                "   \
    GPRINT:4_freq:LAST:"Aktuell\: %5.2lf MHz"                \
    GPRINT:4_freq:AVERAGE:"Mittelwert\: %5.2lf MHz"          \
    GPRINT:4_freq:MAX:"Max\: %5.2lf MHz"                     \
    GPRINT:4_freq:MIN:"Min\: %5.2lf MHz\n"
}


#######################################################################
# Parameter:                                                          #
# $1 Time Range                                                       #
# $2 Filename                                                         #
#######################################################################
printTemp ()
  {
    rrdtool graph $2                                         \
    --title "Temperaturen [°C]"                              \
    --end now --start end-$1                                 \
    -w $WIDTH -h $(($HEIGHT*2)) -a PNG                       \
    --watermark "$WATERMARK"                                 \
    --right-axis 1:0                                         \
    DEF:1_temproom=$RRD:1_temproom:AVERAGE                   \
    DEF:1_tempairflow=$RRD:1_tempairflow:AVERAGE             \
    DEF:1_tempcpu=$RRD:1_tempcpu:AVERAGE                     \
    DEF:2_tempcpu=$RRD:2_tempcpu:AVERAGE                     \
    DEF:3_tempcpu=$RRD:3_tempcpu:AVERAGE                     \
    DEF:4_tempcpu=$RRD:4_tempcpu:AVERAGE                     \
    LINE1:1_tempcpu#0000FF:"Temperatur seti_01      "        \
    GPRINT:1_tempcpu:LAST:"Aktuell\: %5.2lf °C"              \
    GPRINT:1_tempcpu:AVERAGE:"Mittelwert\: %5.2lf °C"        \
    GPRINT:1_tempcpu:MAX:"Max\: %5.2lf °C"                   \
    GPRINT:1_tempcpu:MIN:"Min\: %5.2lf °C\n"                 \
    LINE1:2_tempcpu#00FF00:"Temperatur seti_02      "        \
    GPRINT:2_tempcpu:LAST:"Aktuell\: %5.2lf °C"              \
    GPRINT:2_tempcpu:AVERAGE:"Mittelwert\: %5.2lf °C"        \
    GPRINT:2_tempcpu:MAX:"Max\: %5.2lf °C"                   \
    GPRINT:2_tempcpu:MIN:"Min\: %5.2lf °C\n"                 \
    LINE1:3_tempcpu#FF0000:"Temperatur seti_03      "        \
    GPRINT:3_tempcpu:LAST:"Aktuell\: %5.2lf °C"              \
    GPRINT:3_tempcpu:AVERAGE:"Mittelwert\: %5.2lf °C"        \
    GPRINT:3_tempcpu:MAX:"Max\: %5.2lf °C"                   \
    GPRINT:3_tempcpu:MIN:"Min\: %5.2lf °C\n"                 \
    LINE1:4_tempcpu#FFFF00:"Temperatur seti_04      "        \
    GPRINT:4_tempcpu:LAST:"Aktuell\: %5.2lf °C"              \
    GPRINT:4_tempcpu:AVERAGE:"Mittelwert\: %5.2lf °C"        \
    GPRINT:4_tempcpu:MAX:"Max\: %5.2lf °C"                   \
    GPRINT:4_tempcpu:MIN:"Min\: %5.2lf °C\n"                 \
    LINE1:1_temproom#00FFFF:"Raumtemperatur          "       \
    GPRINT:1_temproom:LAST:"Aktuell\: %5.2lf °C"             \
    GPRINT:1_temproom:AVERAGE:"Mittelwert\: %5.2lf °C"       \
    GPRINT:1_temproom:MAX:"Max\: %5.2lf °C"                  \
    GPRINT:1_temproom:MIN:"Min\: %5.2lf °C\n"                \
    LINE1:1_tempairflow#FF00FF:"Temperatur Airflow      "    \
    GPRINT:1_tempairflow:LAST:"Aktuell\: %5.2lf °C"          \
    GPRINT:1_tempairflow:AVERAGE:"Mittelwert\: %5.2lf °C"    \
    GPRINT:1_tempairflow:MAX:"Max\: %5.2lf °C"               \
    GPRINT:1_tempairflow:MIN:"Min\: %5.2lf °C\n"
 }


#######################################################################
# Parameter:                                                          #
# $1 Time Range                                                       #
# $2 Filename                                                         #
#######################################################################
printHumidity ()
  {
    rrdtool graph $2                                         \
    --title "Luftfeuchtigkeit [% rF]"                        \
    --end now --start end-$1                                 \
    -w $WIDTH -h $HEIGHT -a PNG                              \
    --watermark "$WATERMARK"                                 \
    --right-axis 1:0                                         \
    DEF:1_humidity=$RRD:1_humidity:AVERAGE                   \
    LINE1:1_humidity#0000FF:"Luftfeuchtigkeit"               \
    GPRINT:1_humidity:LAST:"Aktuell\: %5.2lf %% rF"          \
    GPRINT:1_humidity:AVERAGE:"Mittelwert\: %5.2lf %% rF"    \
    GPRINT:1_humidity:MAX:"Max\: %5.2lf %% rF"               \
    GPRINT:1_humidity:MIN:"Min\: %5.2lf %% rF\n"
 }


#######################################################################
# main ################################################################
printLoad "36h", "$PNG_LOAD_D"
printLoad "7d",  "$PNG_LOAD_W"
printLoad "30d", "$PNG_LOAD_M"
printLoad "365d", "$PNG_LOAD_Y"

printFreq "36h", "$PNG_FREQ_D"
printFreq "7d",  "$PNG_FREQ_W"
printFreq "30d", "$PNG_FREQ_M"
printFreq "365d", "$PNG_FREQ_Y"

printTemp "36h", "$PNG_TEMP_D"
printTemp "7d",  "$PNG_TEMP_W"
printTemp "30d", "$PNG_TEMP_M"
printTemp "365d", "$PNG_TEMP_Y"

printHumidity "36h", "$PNG_HUMIDITY_D"
printHumidity "7d",  "$PNG_HUMIDITY_W"
printHumidity "30d", "$PNG_HUMIDITY_M"
printHumidity "365d", "$PNG_HUMIDITY_Y"

mv $PICS/seti_*png $PICS_STORE

# eof #

