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


RRDPATH=$HOME/rrd/
RRD_AP=$RRDPATH/databases/airparticulates.rrd
PICS=$RRDPATH/temp/
PICS_STORE=$RRDPATH/graphs/

WIDTH=1024
HEIGHT=160
WATERMARK=`date  "+%e. %B %Y, %H:%M:%S"`


PNG_AIRPARTICULATES_D=$PICS/airparticulates_d.png
PNG_AIRPARTICULATES_W=$PICS/airparticulates_w.png
PNG_AIRPARTICULATES_M=$PICS/airparticulates_m.png
PNG_AIRPARTICULATES_Y=$PICS/airparticulates_y.png


#######################################################################
# printAirparticulates()                                              #
# Parameter:                                                          #
# $1 Time Range                                                       #
# $2 Filename                                                         #
#######################################################################
printAirparticulates()
  {
    rrdtool graph $2                                           \
    --title "Feinstaub [µg/m3]"                                \
    --end now --start end-$1                                   \
    -w $WIDTH -h $HEIGHT -a PNG                                \
    --watermark "$WATERMARK"                                   \
    --right-axis 1:0                                           \
    DEF:1_pm10=$RRD_AP:1_pm10:AVERAGE                          \
    DEF:1_pm25=$RRD_AP:1_pm25:AVERAGE                          \
    DEF:2_pm10=$RRD_AP:2_pm10:AVERAGE                          \
    DEF:2_pm25=$RRD_AP:2_pm25:AVERAGE                          \
    LINE1:1_pm10#0000FF:"Feinstaub Wien PM10  "                \
    GPRINT:1_pm10:LAST:"\t\tAktuell\: %5.2lf µg/m3"            \
    GPRINT:1_pm10:AVERAGE:"Mittelwert\: %5.2lf µg/m3"          \
    GPRINT:1_pm10:MAX:"Max\: %5.2lf µg/m3"                     \
    GPRINT:1_pm10:MIN:"Min\: %5.2lf µg/m3\n"                   \
    LINE1:1_pm25#33ccff:"Feinstaub Wien PM2,5 "                \
    GPRINT:1_pm25:LAST:"\t\tAktuell\: %5.2lf µg/m3"            \
    GPRINT:1_pm25:AVERAGE:"Mittelwert\: %5.2lf µg/m3"          \
    GPRINT:1_pm25:MAX:"Max\: %5.2lf µg/m3"                     \
    GPRINT:1_pm25:MIN:"Min\: %5.2lf µg/m3\n"                   \
    LINE1:2_pm10#40FF00:"Feinstaub Kollerberg PM10  "          \
    GPRINT:2_pm10:LAST:"\t  Aktuell\: %5.2lf µg/m3"            \
    GPRINT:2_pm10:AVERAGE:"Mittelwert\: %5.2lf µg/m3"          \
    GPRINT:2_pm10:MAX:"Max\: %5.2lf µg/m3"                     \
    GPRINT:2_pm10:MIN:"Min\: %5.2lf µg/m3\n"                   \
    LINE1:2_pm25#ccffcc:"Feinstaub Kollerberg PM2,5 "          \
    GPRINT:2_pm25:LAST:"\t  Aktuell\: %5.2lf µg/m3"            \
    GPRINT:2_pm25:AVERAGE:"Mittelwert\: %5.2lf µg/m3"          \
    GPRINT:2_pm25:MAX:"Max\: %5.2lf µg/m3"                     \
    GPRINT:2_pm25:MIN:"Min\: %5.2lf µg/m3\n"
 }


#######################################################################
# main ################################################################
printAirparticulates "36h", "$PNG_AIRPARTICULATES_D"
printAirparticulates "7d", "$PNG_AIRPARTICULATES_W"
printAirparticulates "30d", "$PNG_AIRPARTICULATES_M"
printAirparticulates "365d", "$PNG_AIRPARTICULATES_Y"

mv $PICS/airparticulates_*png $PICS_STORE

# eof #

