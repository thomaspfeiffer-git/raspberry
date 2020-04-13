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
RRD_PO=$RRDPATH/databases/pool.rrd
PICS=$RRDPATH/temp/
PICS_STORE=$RRDPATH/graphs/

WIDTH=1024
HEIGHT=160
WATERMARK=`date  "+%e. %B %Y, %H:%M:%S"`


PNG_POOLTEMP_D=$RRDPATH/pool_temp_d.png
PNG_POOLTEMP_W=$RRDPATH/pool_temp_w.png
PNG_POOLTEMP_M=$RRDPATH/pool_temp_m.png
PNG_POOLTEMP_Y=$RRDPATH/pool_temp_y.png

PNG_POOLHUMI_D=$RRDPATH/pool_humi_d.png
PNG_POOLHUMI_W=$RRDPATH/pool_humi_w.png
PNG_POOLHUMI_M=$RRDPATH/pool_humi_m.png
PNG_POOLHUMI_Y=$RRDPATH/pool_humi_y.png

PNG_POOLABSHUMI_D=$RRDPATH/pool_abshumi_d.png
PNG_POOLABSHUMI_W=$RRDPATH/pool_abshumi_w.png
PNG_POOLABSHUMI_M=$RRDPATH/pool_abshumi_m.png
PNG_POOLABSHUMI_Y=$RRDPATH/pool_abshumi_y.png

PNG_POOLFANS_D=$RRDPATH/pool_fans_d.png
PNG_POOLFANS_W=$RRDPATH/pool_fans_w.png
PNG_POOLFANS_M=$RRDPATH/pool_fans_m.png
PNG_POOLFANS_Y=$RRDPATH/pool_fans_y.png


#######################################################################
# printPoolTemp()                                                     #
# Parameter:                                                          #
# $1 Time Range                                                       #
# $2 Filename                                                         #
#######################################################################
printPoolTemp()
  {
    rrdtool graph $2                                           \
    --title "Pool Kollerberg: Temperaturen"                    \
    --end now --start end-$1                                   \
    -w $WIDTH -h $HEIGHT -a PNG                                \
    --watermark "$WATERMARK"                                   \
    --right-axis 1:0                                           \
    DEF:temp_box=$RRD_PO:TEMPBOX:AVERAGE                       \
    DEF:temp_airin=$RRD_PO:TEMPAIRIN:AVERAGE                   \
    DEF:temp_airout=$RRD_PO:TEMPAIROUT:AVERAGE                 \
    DEF:temp_outdoor=$RRD_PO:TEMPOUTDOOR:AVERAGE               \
    DEF:temp_room=$RRD_PO:TEMPROOM:AVERAGE                     \
    DEF:temp_water=$RRD_PO:TEMPWATER:AVERAGE                   \
    LINE1:temp_box#BE25EB:"Temperatur Steuerbox          "     \
    GPRINT:temp_box:LAST:"Aktuell\: %5.2lf °C"                 \
    GPRINT:temp_box:AVERAGE:"Mittelwert\: %5.2lf °C"           \
    GPRINT:temp_box:MAX:"Max\: %5.2lf °C"                      \
    GPRINT:temp_box:MIN:"Min\: %5.2lf °C\n"                    \
    LINE1:temp_airin#009900:"Temperatur einströmende Luft  "   \
    GPRINT:temp_airin:LAST:"Aktuell\: %5.2lf °C"               \
    GPRINT:temp_airin:AVERAGE:"Mittelwert\: %5.2lf °C"         \
    GPRINT:temp_airin:MAX:"Max\: %5.2lf °C"                    \
    GPRINT:temp_airin:MIN:"Min\: %5.2lf °C\n"                  \
    LINE1:temp_airout#FF4242:"Temperatur ausströmende Luft  "  \
    GPRINT:temp_airout:LAST:"Aktuell\: %5.2lf °C"              \
    GPRINT:temp_airout:AVERAGE:"Mittelwert\: %5.2lf °C"        \
    GPRINT:temp_airout:MAX:"Max\: %5.2lf °C"                   \
    GPRINT:temp_airout:MIN:"Min\: %5.2lf °C\n"                 \
    LINE1:temp_outdoor#3336F0:"Temperatur außen              " \
    GPRINT:temp_outdoor:LAST:"Aktuell\: %5.2lf °C"             \
    GPRINT:temp_outdoor:AVERAGE:"Mittelwert\: %5.2lf °C"       \
    GPRINT:temp_outdoor:MAX:"Max\: %5.2lf °C"                  \
    GPRINT:temp_outdoor:MIN:"Min\: %5.2lf °C\n"                \
    LINE1:temp_room#000000:"Temperatur innen              "    \
    GPRINT:temp_room:LAST:"Aktuell\: %5.2lf °C"                \
    GPRINT:temp_room:AVERAGE:"Mittelwert\: %5.2lf °C"          \
    GPRINT:temp_room:MAX:"Max\: %5.2lf °C"                     \
    GPRINT:temp_room:MIN:"Min\: %5.2lf °C\n"                   \
    LINE1:temp_water#2AF9FC:"Temperatur Wasser             "   \
    GPRINT:temp_water:LAST:"Aktuell\: %5.2lf °C"               \
    GPRINT:temp_water:AVERAGE:"Mittelwert\: %5.2lf °C"         \
    GPRINT:temp_water:MAX:"Max\: %5.2lf °C"                    \
    GPRINT:temp_water:MIN:"Min\: %5.2lf °C\n"                  &
 }


#######################################################################
# printPoolHumi()                                                     #
# Parameter:                                                          #
# $1 Time Range                                                       #
# $2 Filename                                                         #
#######################################################################
printPoolHumi()
  {
    rrdtool graph $2                                              \
    --title "Pool Kollerberg: Luftfeuchtigkeit"                   \
    --end now --start end-$1                                      \
    -w $WIDTH -h $HEIGHT -a PNG                                   \
    --watermark "$WATERMARK"                                      \
    --right-axis 1:0                                              \
    DEF:humi_box=$RRD_PO:HUMIBOX:AVERAGE                          \
    DEF:humi_airin=$RRD_PO:HUMIAIRIN:AVERAGE                      \
    DEF:humi_airout=$RRD_PO:HUMIAIROUT:AVERAGE                    \
    LINE1:humi_box#BE25EB:"Luftfeuchtigkeit Steuerbox        "    \
    GPRINT:humi_box:LAST:"\t Aktuell\: %5.2lf %%"                 \
    GPRINT:humi_box:AVERAGE:"Mittelwert\: %5.2lf %%"              \
    GPRINT:humi_box:MAX:"Max\: %5.2lf %%"                         \
    GPRINT:humi_box:MIN:"Min\: %5.2lf %%\n"                       \
    LINE1:humi_airin#009900:"Luftfeuchtigkeit einströmende Luft"  \
    GPRINT:humi_airin:LAST:"\t Aktuell\: %5.2lf %%"               \
    GPRINT:humi_airin:AVERAGE:"Mittelwert\: %5.2lf %%"            \
    GPRINT:humi_airin:MAX:"Max\: %5.2lf %%"                       \
    GPRINT:humi_airin:MIN:"Min\: %5.2lf %%\n"                     \
    LINE1:humi_airout#FF4242:"Luftfeuchtigkeit ausströmende Luft" \
    GPRINT:humi_airout:LAST:"\t Aktuell\: %5.2lf %%"              \
    GPRINT:humi_airout:AVERAGE:"Mittelwert\: %5.2lf %%"           \
    GPRINT:humi_airout:MAX:"Max\: %5.2lf %%"                      \
    GPRINT:humi_airout:MIN:"Min\: %5.2lf %%\n"                    &
 }


#######################################################################
# printPoolAbsHumi()                                                  #
# Parameter:                                                          #
# $1 Time Range                                                       #
# $2 Filename                                                         #
#######################################################################
printPoolAbsHumi()
  {
    rrdtool graph $2                                              \
    --title "Pool Kollerberg: Absolute Luftfeuchtigkeit"          \
    --end now --start end-$1                                      \
    -w $WIDTH -h $HEIGHT -a PNG                                   \
    --watermark "$WATERMARK"                                      \
    --right-axis 1:0                                              \
    DEF:abshumi_box=$RRD_PO:ABSHUBOX:AVERAGE                      \
    DEF:abshumi_airin=$RRD_PO:ABSHUAIRIN:AVERAGE                  \
    DEF:abshumi_airout=$RRD_PO:ABSHUAIROUT:AVERAGE              \
    LINE1:abshumi_box#BE25EB:"Luftfeuchtigkeit absolut Steuerbox        "    \
    GPRINT:abshumi_box:LAST:"\t Aktuell\: %5.2lf g/m^3"                 \
    GPRINT:abshumi_box:AVERAGE:"Mittelwert\: %5.2lf g/m^3"              \
    GPRINT:abshumi_box:MAX:"Max\: %5.2lf g/m^3"                         \
    GPRINT:abshumi_box:MIN:"Min\: %5.2lf g/m^3\n"                       \
    LINE1:abshumi_airin#009900:"Luftfeuchtigkeit absolut einströmende Luft"  \
    GPRINT:abshumi_airin:LAST:"\t Aktuell\: %5.2lf g/m^3"               \
    GPRINT:abshumi_airin:AVERAGE:"Mittelwert\: %5.2lf g/m^3"            \
    GPRINT:abshumi_airin:MAX:"Max\: %5.2lf g/m^3"                       \
    GPRINT:abshumi_airin:MIN:"Min\: %5.2lf g/m^3\n"                     \
    LINE1:abshumi_airout#FF4242:"Luftfeuchtigkeit absolut ausströmende Luft" \
    GPRINT:abshumi_airout:LAST:"\t Aktuell\: %5.2lf g/m^3"              \
    GPRINT:abshumi_airout:AVERAGE:"Mittelwert\: %5.2lf g/m^3"           \
    GPRINT:abshumi_airout:MAX:"Max\: %5.2lf g/m^3"                      \
    GPRINT:abshumi_airout:MIN:"Min\: %5.2lf g/m^3\n"                    &
}


#######################################################################
# printPoolFans()                                                     #
# Parameter:                                                          #
# $1 Time Range                                                       #
# $2 Filename                                                         #
#######################################################################
printPoolFans()
  {
    rrdtool graph $2                                              \
    --title "Pool Kollerberg: Fans"                               \
    --end now --start end-$1                                      \
    -w $WIDTH -h $HEIGHT -a PNG                                   \
    --watermark "$WATERMARK"                                      \
    --right-axis 1:0                                              \
    DEF:fan1=$RRD_PO:FAN1:AVERAGE                                 \
    DEF:fan2=$RRD_PO:FAN2:AVERAGE                                 \
    DEF:fan3=$RRD_PO:FAN3:AVERAGE                                 \
    DEF:fan4=$RRD_PO:FAN4:AVERAGE                                 \
    AREA:fan1#42C3FF:"Fan einströmende Luft #1 "                  \
    GPRINT:fan1:LAST:"\t Aktuell\: %5.0lf"                        \
    GPRINT:fan1:AVERAGE:"Mittelwert\: %5.2lf\n"                   \
    STACK:fan4#F6FC2A:"Fan einströmende Luft #2 "                 \
    GPRINT:fan4:LAST:"\t Aktuell\: %5.0lf"                        \
    GPRINT:fan4:AVERAGE:"Mittelwert\: %5.2lf\n"                   \
    STACK:fan2#FF4242:"Fan ausströmende Luft    "                 \
    GPRINT:fan2:LAST:"\t Aktuell\: %5.0lf"                        \
    GPRINT:fan2:AVERAGE:"Mittelwert\: %5.2lf\n"                   \
    STACK:fan3#BE25EB:"Fan Steuerbox            "                 \
    GPRINT:fan3:LAST:"\t Aktuell\: %5.0lf"                        \
    GPRINT:fan3:AVERAGE:"Mittelwert\: %5.2lf\n"                   &
 }


#######################################################################
# main ################################################################
printPoolTemp "36h", "$PNG_POOLTEMP_D"
printPoolTemp "7d", "$PNG_POOLTEMP_W"
printPoolTemp "30d", "$PNG_POOLTEMP_M"
printPoolTemp "365d", "$PNG_POOLTEMP_Y"

printPoolHumi "36h", "$PNG_POOLHUMI_D"
printPoolHumi "7d", "$PNG_POOLHUMI_W"
printPoolHumi "30d", "$PNG_POOLHUMI_M"
printPoolHumi "365d", "$PNG_POOLHUMI_Y"

printPoolAbsHumi "36h", "$PNG_POOLABSHUMI_D"
printPoolAbsHumi "7d", "$PNG_POOLABSHUMI_W"
printPoolAbsHumi "30d", "$PNG_POOLABSHUMI_M"
printPoolAbsHumi "365d", "$PNG_POOLABSHUMI_Y"

printPoolFans "36h", "$PNG_POOLFANS_D"
printPoolFans "7d", "$PNG_POOLFANS_W"
printPoolFans "30d", "$PNG_POOLFANS_M"
printPoolFans "365d", "$PNG_POOLFANS_Y"

mv $PICS/pool_*png $PICS_STORE

# eof #

