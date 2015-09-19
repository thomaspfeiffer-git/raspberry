#/bin/bash

RRDPATH=/schild/weather/
RRD_H=$RRDPATH/hibernation.rrd

PNG_TEMP_D=$RRDPATH/hibernation_temp_d.png
PNG_TEMP_W=$RRDPATH/hibernation_temp_w.png
PNG_TEMP_M=$RRDPATH/hibernation_temp_m.png
PNG_TEMP_Y=$RRDPATH/hibernation_temp_y.png

PNG_HUMI_D=$RRDPATH/hibernation_humi_d.png
PNG_HUMI_W=$RRDPATH/hibernation_humi_w.png
PNG_HUMI_M=$RRDPATH/hibernation_humi_m.png
PNG_HUMI_Y=$RRDPATH/hibernation_humi_y.png

PNG_CPU_D=$RRDPATH/hibernation_cpu_temp_d.png
PNG_CPU_W=$RRDPATH/hibernation_cpu_temp_w.png
PNG_CPU_M=$RRDPATH/hibernation_cpu_temp_m.png
PNG_CPU_Y=$RRDPATH/hibernation_cpu_temp_y.png

PNG_FRIDGE_D=$RRDPATH/hibernation_fridge_d.png
PNG_FRIDGE_W=$RRDPATH/hibernation_fridge_w.png
PNG_FRIDGE_M=$RRDPATH/hibernation_fridge_m.png
PNG_FRIDGE_Y=$RRDPATH/hibernation_fridge_y.png


WIDTH=1024
HEIGHT=160
WATERMARK=`date  "+%e. %B %Y, %H:%M:%S"`




#######################################################################
# printTemp()                                                         #
# Parameter:                                                          #
# $1 Time Range                                                       #
# $2 Filename                                                         #
#######################################################################
printTemp ()
  {
    rrdtool graph $2                                       \
    --title "Temperatur [°C]"                              \
    --end now --start end-$1                               \
    -w $WIDTH -h $(($HEIGHT*2)) -a PNG                     \
    --watermark "$WATERMARK"                               \
    --right-axis 1:0                                       \
    DEF:hibernation_temp1=$RRD_H:hibernation_temp1:AVERAGE  \
    LINE1:hibernation_temp1#2ECCFA:"Temperatur Sensor 1"    \
    GPRINT:hibernation_temp1:LAST:"Aktuell\: %5.2lf °C"         \
    GPRINT:hibernation_temp1:AVERAGE:"Mittelwert\: %5.2lf °C"   \
    GPRINT:hibernation_temp1:MAX:"Max\: %5.2lf °C"              \
    GPRINT:hibernation_temp1:MIN:"Min\: %5.2lf °C\n"            \
    DEF:hibernation_temp2=$RRD_H:hibernation_temp2:AVERAGE  \
    LINE1:hibernation_temp2##0040FF:"Temperatur Sensor 2"    \
    GPRINT:hibernation_temp2:LAST:"Aktuell\: %5.2lf °C"         \
    GPRINT:hibernation_temp2:AVERAGE:"Mittelwert\: %5.2lf °C"   \
    GPRINT:hibernation_temp2:MAX:"Max\: %5.2lf °C"              \
    GPRINT:hibernation_temp2:MIN:"Min\: %5.2lf °C\n"
 }


#######################################################################
# printCPUTemp()                                                      #
# Parameter:                                                          #
# $1 Time Range                                                       #
# $2 Filename                                                         #
#######################################################################
printCPUTemp ()
  {
    rrdtool graph $2                                            \
    --title "Temperatur Raspberry Pi [°C]"                      \
    --end now --start end-$1                                    \
    -w $WIDTH -h $HEIGHT -a PNG                                 \
    --watermark "$WATERMARK"                                    \
    --right-axis 1:0                                            \
    DEF:hibernation_tempcpu=$RRD_H:hibernation_tempcpu:AVERAGE    \
    LINE1:hibernation_tempcpu#FF00FF:"Temperatur Raspberry Pi"  \
    GPRINT:hibernation_tempcpu:LAST:"\t\t Aktuell\: %5.2lf %%"  \
    GPRINT:hibernation_tempcpu:AVERAGE:"Mittelwert\: %5.2lf %%" \
    GPRINT:hibernation_tempcpu:MAX:"Max\: %5.2lf %%"            \
    GPRINT:hibernation_tempcpu:MIN:"Min\: %5.2lf %%\n"
 }



#######################################################################
# printFridge()                                                       #
# Parameter:                                                          #
# $1 Time Range                                                       #
# $2 Filename                                                         #
#######################################################################
printFridge ()
  {
    rrdtool graph $2                                            \
    --title "Kühlschrank kühlt; Türe offen"                     \
    --end now --start end-$1                                    \
    -w $WIDTH -h $(($HEIGHT/2)) -a PNG                          \
    --watermark "$WATERMARK"                                    \
    --alt-y-grid                                                \
    --right-axis 1:0                                            \
    DEF:hibernation_on=$RRD_H:hibernation_on:AVERAGE            \
    DEF:hibernation_open=$RRD_H:hibernation_open:AVERAGE        \
    AREA:hibernation_on#0000FF:"Kühlschrank kühlt\t"        \
    GPRINT:hibernation_on:LAST:"\t Aktuell\: %5.0lf"            \
    GPRINT:hibernation_on:AVERAGE:"Mittelwert\: %5.2lf\n"       \
    STACK:hibernation_open#FF0000:"Türe offen\t"                \
    GPRINT:hibernation_open:LAST:"\t Aktuell\: %5.0lf"          \
    GPRINT:hibernation_open:AVERAGE:"Mittelwert\: %5.2lf\n"
 }







printTemp "36h", "$PNG_TEMP_D"
printTemp "7d",  "$PNG_TEMP_W"
printTemp "30d", "$PNG_TEMP_M"
printTemp "365d", "$PNG_TEMP_Y"

printCPUTemp "36h", "$PNG_CPU_D"
printCPUTemp "7d",  "$PNG_CPU_W"
printCPUTemp "30d", "$PNG_CPU_M"
printCPUTemp "365d", "$PNG_CPU_Y"

printFridge "36h", "$PNG_FRIDGE_D"
printFridge "7d", "$PNG_FRIDGE_W"
printFridge "30d", "$PNG_FRIDGE_M"
printFridge "365d", "$PNG_FRIDGE_Y"


