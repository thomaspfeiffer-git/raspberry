#/bin/bash

RRDPATH=/schild/weather/
RRD=$RRDPATH/seti.rrd

WIDTH=1024
HEIGHT=160
WATERMARK=`date  "+%e. %B %Y, %H:%M:%S"`

PNG_LOAD_D=$RRDPATH/load_d.png
PNG_LOAD_W=$RRDPATH/load_w.png
PNG_LOAD_M=$RRDPATH/load_m.png
PNG_LOAD_Y=$RRDPATH/load_y.png

PNG_TEMPCPU_D=$RRDPATH/tempcpu_d.png
PNG_TEMPCPU_W=$RRDPATH/tempcpu_w.png
PNG_TEMPCPU_M=$RRDPATH/tempcpu_m.png
PNG_TEMPCPU_Y=$RRDPATH/tempcpu_y.png


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
    LINE1:1_load#0000FF:"Load seti_01                    "   \
    GPRINT:1_load:LAST:"Aktuell\: %5.2lf °C"                 \
    GPRINT:1_load:AVERAGE:"Mittelwert\: %5.2lf °C"           \
    GPRINT:1_load:MAX:"Max\: %5.2lf °C"                      \
    GPRINT:1_load:MIN:"Min\: %5.2lf °C\n"                    \
    LINE1:2_load#00FF00:"Load seti_02                    "   \
    GPRINT:2_load:LAST:"Aktuell\: %5.2lf °C"                 \
    GPRINT:2_load:AVERAGE:"Mittelwert\: %5.2lf °C"           \
    GPRINT:2_load:MAX:"Max\: %5.2lf °C"                      \
    GPRINT:2_load:MIN:"Min\: %5.2lf °C\n"                    \
    LINE1:3_load#FF0000:"Load seti_03                    "   \
    GPRINT:3_load:LAST:"Aktuell\: %5.2lf °C"                 \
    GPRINT:3_load:AVERAGE:"Mittelwert\: %5.2lf °C"           \
    GPRINT:3_load:MAX:"Max\: %5.2lf °C"                      \
    GPRINT:3_load:MIN:"Min\: %5.2lf °C\n"                    \
    LINE1:1_load#FFFF00:"Load seti_04                    "   \
    GPRINT:4_load:LAST:"Aktuell\: %5.2lf °C"                 \
    GPRINT:4_load:AVERAGE:"Mittelwert\: %5.2lf °C"           \
    GPRINT:4_load:MAX:"Max\: %5.2lf °C"                      \
    GPRINT:4_load:MIN:"Min\: %5.2lf °C\n"                    &
 }


#######################################################################
# Parameter:                                                          #
# $1 Time Range                                                       #
# $2 Filename                                                         #
#######################################################################
printTempCPU ()
  {
    rrdtool graph $2                                         \
    --title "Temperature CPU [°C]"                           \
    --end now --start end-$1                                 \
    -w $WIDTH -h $(($HEIGHT*2)) -a PNG                       \
    --watermark "$WATERMARK"                                 \
    --right-axis 1:0                                         \
    DEF:1_tempcpu=$RRD:1_tempcpu:AVERAGE                     \
    DEF:2_tempcpu=$RRD:2_tempcpu:AVERAGE                     \
    DEF:3_tempcpu=$RRD:3_tempcpu:AVERAGE                     \
    DEF:4_tempcpu=$RRD:4_tempcpu:AVERAGE                     \
    LINE1:1_tempcpu#0000FF:"Temperatur seti_01           "   \
    GPRINT:1_tempcpu:LAST:"Aktuell\: %5.2lf °C"              \
    GPRINT:1_tempcpu:AVERAGE:"Mittelwert\: %5.2lf °C"        \
    GPRINT:1_tempcpu:MAX:"Max\: %5.2lf °C"                   \
    GPRINT:1_tempcpu:MIN:"Min\: %5.2lf °C\n"                 \
    LINE1:2_tempcpu#00FF00:"Temperatur seti_02           "   \
    GPRINT:2_tempcpu:LAST:"Aktuell\: %5.2lf °C"              \
    GPRINT:2_tempcpu:AVERAGE:"Mittelwert\: %5.2lf °C"        \
    GPRINT:2_tempcpu:MAX:"Max\: %5.2lf °C"                   \
    GPRINT:2_tempcpu:MIN:"Min\: %5.2lf °C\n"                 \
    LINE1:3_tempcpu#FF0000:"Temperatur seti_03           "   \
    GPRINT:3_tempcpu:LAST:"Aktuell\: %5.2lf °C"              \
    GPRINT:3_tempcpu:AVERAGE:"Mittelwert\: %5.2lf °C"        \
    GPRINT:3_tempcpu:MAX:"Max\: %5.2lf °C"                   \
    GPRINT:3_tempcpu:MIN:"Min\: %5.2lf °C\n"                 \
    LINE1:4_tempcpu#FFFF00:"Temperatur seti_04           "   \
    GPRINT:4_tempcpu:LAST:"Aktuell\: %5.2lf °C"              \
    GPRINT:4_tempcpu:AVERAGE:"Mittelwert\: %5.2lf °C"        \
    GPRINT:4_tempcpu:MAX:"Max\: %5.2lf °C"                   \
    GPRINT:4_tempcpu:MIN:"Min\: %5.2lf °C\n"                 &
 }


#######################################################################
# main ################################################################
printLoad "36h", "$PNG_LOAD_D"
printLoad "7d",  "$PNG_LOAD_W"
printLoad "30d", "$PNG_LOAD_M"
printLoad "365d", "$PNG_LOAD_Y"

printTempCPU "36h", "$PNG_TEMPCPU_D"
printTempCPU "7d",  "$PNG_TEMPCPU_W"
printTempCPU "30d", "$PNG_TEMPCPU_M"
printTempCPU "365d", "$PNG_TEMPCPU_Y"



# eof #

