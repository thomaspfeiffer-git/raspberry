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
RRD_AP=$RRDPATH/databases/solar.rrd
PICS=$RRDPATH/temp/
PICS_STORE=$RRDPATH/graphs/

WIDTH=1024
HEIGHT=480
WATERMARK=`date  "+%e. %B %Y, %H:%M:%S"`


PNG_SOLAR_D=$PICS/solar_d.png
PNG_SOLAR_W=$PICS/solar_w.png
PNG_SOLAR_M=$PICS/solar_m.png
PNG_SOLAR_Y=$PICS/solar_y.png


#######################################################################
# printSolar()                                                        #
# Parameter:                                                          #
# $1 Time Range                                                       #
# $2 Filename                                                         #
#######################################################################
printSolar()
  {
    rrdtool graph $2                                           \
    --title "Leistung [W]"                                     \
    --end now --start end-$1                                   \
    -w $WIDTH -h $HEIGHT -a PNG                                \
    --watermark "$WATERMARK"                                   \
    --right-axis 1:0                                           \
    DEF:Main_P=$RRD_AP:Main_P:AVERAGE                          \
    DEF:Solar_P=$RRD_AP:Solar_P:AVERAGE                        \
    LINE1:Main_P#FF0000:"Leistung EVN  "                       \
    GPRINT:Main_P:LAST:"\t\tAktuell\: %5.2lf W"                \
    GPRINT:Main_P:AVERAGE:"Mittelwert\: %5.2lf W"              \
    GPRINT:Main_P:MAX:"Max\: %5.2lf W"                         \
    GPRINT:Main_P:MIN:"Min\: %5.2lf W\n"                       \
    LINE1:Solar_P#FFE933:"Leistung Sonne"                      \
    GPRINT:Solar_P:LAST:"\t\tAktuell\: %5.2lf W"               \
    GPRINT:Solar_P:AVERAGE:"Mittelwert\: %5.2lf W"             \
    GPRINT:Solar_P:MAX:"Max\: %5.2lf W"                        \
    GPRINT:Solar_P:MIN:"Min\: %5.2lf W\n"                      \
    HRULE:0#0000FF
}

#######################################################################
# main ################################################################
printSolar "36h", "$PNG_SOLAR_D"
printSolar "7d", "$PNG_SOLAR_W"
printSolar "30d", "$PNG_SOLAR_M"
printSolar "365d", "$PNG_SOLAR_Y"

mv $PICS/solar_*png $PICS_STORE

# eof #

