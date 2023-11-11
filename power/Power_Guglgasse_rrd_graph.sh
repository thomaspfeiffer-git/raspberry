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
RRD_AP=$RRDPATH/databases/power_guglgasse.rrd
PICS=$RRDPATH/temp/
PICS_STORE=$RRDPATH/graphs/

WIDTH=1024
HEIGHT=480
WATERMARK=`date  "+%e. %B %Y, %H:%M:%S"`


PNG_POWER_GUGLGASSE_D=$PICS/power_guglgasse_d.png
PNG_POWER_GUGLGASSE_W=$PICS/power_guglgasse_w.png
PNG_POWER_GUGLGASSE_M=$PICS/power_guglgasse_m.png
PNG_POWER_GUGLGASSE_Y=$PICS/power_guglgasse_y.png


#######################################################################
# printPowerGuglgasse()                                               #
# Parameter:                                                          #
# $1 Time Range                                                       #
# $2 Filename                                                         #
#######################################################################
printPowerGuglgasse()
  {
    rrdtool graph $2                                           \
    --title "Leistung [W]"                                     \
    --end now --start end-$1                                   \
    -w $WIDTH -h $HEIGHT -a PNG                                \
    --watermark "$WATERMARK"                                   \
    --right-axis 1:0                                           \
    DEF:Main_P=$RRD_AP:Main_P:AVERAGE                          \
    LINE1:Main_P#FF0000:"Leistung "                            \
    GPRINT:Main_P:LAST:"\t\tAktuell\: %5.2lf W"                \
    GPRINT:Main_P:AVERAGE:"Mittelwert\: %5.2lf W"              \
    GPRINT:Main_P:MAX:"Max\: %5.2lf W"                         \
    GPRINT:Main_P:MIN:"Min\: %5.2lf W\n"                       \
    LINE1:0#0000FF
}

#######################################################################
# main ################################################################
printPowerGuglgasse "36h", "$PNG_POWER_GUGLGASSE_D"
printPowerGuglgasse "7d", "$PNG_POWER_GUGLGASSE_W"
printPowerGuglgasse "30d", "$PNG_POWER_GUGLGASSE_M"
printPowerGuglgasse "365d", "$PNG_POWER_GUGLGASSE_Y"

mv $PICS/power_guglgasse_*png $PICS_STORE

# eof #

