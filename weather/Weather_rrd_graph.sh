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
RRD_IN=$RRDPATH/databases/weather_indoor.rrd
RRD_OUT=$RRDPATH/databases/weather_outdoor.rrd
RRD_K=$RRDPATH/databases/kidsroom.rrd
RRD_KB=$RRDPATH/databases/weather_kollerberg.rrd
RRD_WR=$RRDPATH/databases/wardrobe.rrd
RRD_AR=$RRDPATH/databases/anteroom.rrd
RRD_KI=$RRDPATH/databases/kitchen.rrd
RRD_SR=$RRDPATH/databases/serverroom.rrd
RRD_PO=$RRDPATH/databases/pool.rrd

PICS=$RRDPATH/temp/weather/
PICS_STORE=$RRDPATH/graphs/


PNG_TEMP_D=$PICS/weather_temp_d.png
PNG_TEMP_W=$PICS/weather_temp_w.png
PNG_TEMP_M=$PICS/weather_temp_m.png
PNG_TEMP_Y=$PICS/weather_temp_y.png

PNG_HUMI_D=$PICS/weather_humi_d.png
PNG_HUMI_W=$PICS/weather_humi_w.png
PNG_HUMI_M=$PICS/weather_humi_m.png
PNG_HUMI_Y=$PICS/weather_humi_y.png

PNG_PRES_D=$PICS/weather_pressure_d.png
PNG_PRES_W=$PICS/weather_pressure_w.png
PNG_PRES_M=$PICS/weather_pressure_m.png
PNG_PRES_Y=$PICS/weather_pressure_y.png

PNG_CPU_D=$PICS/cpu_temp_d.png
PNG_CPU_W=$PICS/cpu_temp_w.png
PNG_CPU_M=$PICS/cpu_temp_m.png
PNG_CPU_Y=$PICS/cpu_temp_y.png

PNG_WARDROBE_D=$PICS/wardrobe_d.png
PNG_WARDROBE_W=$PICS/wardrobe_w.png
PNG_WARDROBE_M=$PICS/wardrobe_m.png
PNG_WARDROBE_Y=$PICS/wardrobe_y.png

PNG_WR_LIGHTNESS_D=$PICS/wr_lightness_d.png
PNG_WR_LIGHTNESS_W=$PICS/wr_lightness_w.png
PNG_WR_LIGHTNESS_M=$PICS/wr_lightness_m.png
PNG_WR_LIGHTNESS_Y=$PICS/wr_lightness_y.png

PNG_ANTEROOM_D=$PICS/anteroom_d.png
PNG_ANTEROOM_W=$PICS/anteroom_w.png
PNG_ANTEROOM_M=$PICS/anteroom_m.png
PNG_ANTEROOM_Y=$PICS/anteroom_y.png

PNG_AIRQUALITY_D=$PICS/airquality_d.png
PNG_AIRQUALITY_W=$PICS/airquality_w.png
PNG_AIRQUALITY_M=$PICS/airquality_m.png
PNG_AIRQUALITY_Y=$PICS/airquality_y.png

PNG_AIRPARTICULATES_D=$PICS/airparticulates_d.png
PNG_AIRPARTICULATES_W=$PICS/airparticulates_w.png
PNG_AIRPARTICULATES_M=$PICS/airparticulates_m.png
PNG_AIRPARTICULATES_Y=$PICS/airparticulates_y.png

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
    DEF:temp_outdoor=$RRD_OUT:temp:AVERAGE                   \
    DEF:temp_realoutdoor=$RRD_OUT:temp_gard:AVERAGE          \
    DEF:temp_indoor=$RRD_IN:temp:AVERAGE                     \
    DEF:ki_temp=$RRD_KI:ki_temp:AVERAGE                      \
    DEF:kidsroom_temp1=$RRD_K:kidsroom_temp1:AVERAGE         \
    DEF:wr_temp1=$RRD_WR:wr_temp1:AVERAGE                    \
    DEF:sr_temp=$RRD_SR:temp:AVERAGE                         \
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
    LINE1:ki_temp#C8FE2E:"Temperatur Küche              "    \
    GPRINT:ki_temp:LAST:"Aktuell\: %5.2lf °C"                \
    GPRINT:ki_temp:AVERAGE:"Mittelwert\: %5.2lf °C"          \
    GPRINT:ki_temp:MAX:"Max\: %5.2lf °C"                     \
    GPRINT:ki_temp:MIN:"Min\: %5.2lf °C\n"                   \
    LINE1:kidsroom_temp1#00ccff:"Temperatur Kinderzimmer       " \
    GPRINT:kidsroom_temp1:LAST:"Aktuell\: %5.2lf °C"         \
    GPRINT:kidsroom_temp1:AVERAGE:"Mittelwert\: %5.2lf °C"   \
    GPRINT:kidsroom_temp1:MAX:"Max\: %5.2lf °C"              \
    GPRINT:kidsroom_temp1:MIN:"Min\: %5.2lf °C\n"            \
    LINE1:wr_temp1#ffcc00:"Temperatur Kleiderkasten      "   \
    GPRINT:wr_temp1:LAST:"Aktuell\: %5.2lf °C"               \
    GPRINT:wr_temp1:AVERAGE:"Mittelwert\: %5.2lf °C"         \
    GPRINT:wr_temp1:MAX:"Max\: %5.2lf °C"                    \
    GPRINT:wr_temp1:MIN:"Min\: %5.2lf °C\n"                  \
    LINE1:sr_temp#000000:"Temperatur Serverraum         "    \
    GPRINT:sr_temp:LAST:"Aktuell\: %5.2lf °C"                \
    GPRINT:sr_temp:AVERAGE:"Mittelwert\: %5.2lf °C"          \
    GPRINT:sr_temp:MAX:"Max\: %5.2lf °C"                     \
    GPRINT:sr_temp:MIN:"Min\: %5.2lf °C\n"                   \
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
    --title "Temperatur Pis [°C]"                                        \
    --end now --start end-$1                                             \
    -w $WIDTH -h $HEIGHT -a PNG                                          \
    --watermark "$WATERMARK"                                             \
    --right-axis 1:0                                                     \
    DEF:in_tempcpu=$RRD_IN:temp_cpu:AVERAGE                              \
    DEF:ki_tempcpu=$RRD_KI:ki_tempcpu:AVERAGE                            \
    DEF:kidsroom_tempcpu=$RRD_K:kidsroom_tempcpu:AVERAGE                 \
    DEF:wr_tempcpu=$RRD_WR:wr_tempcpu:AVERAGE                            \
    DEF:ar_tempcpu=$RRD_AR:ar_tempcpu:AVERAGE                            \
    DEF:sr_tempcpu=$RRD_SR:tempcpu:AVERAGE                               \
    DEF:out_tempcpu=$RRD_OUT:temp_cpu:AVERAGE                            \
    DEF:kb_i_tcpu=$RRD_KB:kb_i_tcpu:AVERAGE                              \
    DEF:kb_a_tcpu=$RRD_KB:kb_a_tcpu:AVERAGE                              \
    DEF:kb_k_tcpu=$RRD_KB:kb_k_tcpu:AVERAGE                              \
    DEF:po_tempcpu=$RRD_PO:TEMPCPU:AVERAGE                               \
    LINE1:in_tempcpu#FF0000:"Temperatur NanoPi NEO Air Wohnzimmer     "  \
    GPRINT:in_tempcpu:LAST:"\t Aktuell\: %5.2lf °C"                      \
    GPRINT:in_tempcpu:AVERAGE:"Mittelwert\: %5.2lf °C"                   \
    GPRINT:in_tempcpu:MAX:"Max\: %5.2lf °C"                              \
    GPRINT:in_tempcpu:MIN:"Min\: %5.2lf °C\n"                            \
    LINE1:ki_tempcpu#C8FE2E:"Temperatur Raspberry Pi Küche            "  \
    GPRINT:ki_tempcpu:LAST:"\t Aktuell\: %5.2lf °C"                      \
    GPRINT:ki_tempcpu:AVERAGE:"Mittelwert\: %5.2lf °C"                   \
    GPRINT:ki_tempcpu:MAX:"Max\: %5.2lf °C"                              \
    GPRINT:ki_tempcpu:MIN:"Min\: %5.2lf °C\n"                            \
    LINE1:kidsroom_tempcpu#00ccff:"Temperatur Raspberry Pi Kinderzimmer     " \
    GPRINT:kidsroom_tempcpu:LAST:"\t Aktuell\: %5.2lf °C"                \
    GPRINT:kidsroom_tempcpu:AVERAGE:"Mittelwert\: %5.2lf °C"             \
    GPRINT:kidsroom_tempcpu:MAX:"Max\: %5.2lf °C"                        \
    GPRINT:kidsroom_tempcpu:MIN:"Min\: %5.2lf °C\n"                      \
    LINE1:ar_tempcpu#ff1493:"Temperatur NanoPi NEO Air Vorzimmer      "  \
    GPRINT:ar_tempcpu:LAST:"\t Aktuell\: %5.2lf °C"                      \
    GPRINT:ar_tempcpu:AVERAGE:"Mittelwert\: %5.2lf °C"                   \
    GPRINT:ar_tempcpu:MAX:"Max\: %5.2lf °C"                              \
    GPRINT:ar_tempcpu:MIN:"Min\: %5.2lf °C\n"                            \
    LINE1:sr_tempcpu#000000:"Temperatur NanoPi NEO Serverraum         "  \
    GPRINT:sr_tempcpu:LAST:"\t Aktuell\: %5.2lf °C"                      \
    GPRINT:sr_tempcpu:AVERAGE:"Mittelwert\: %5.2lf °C"                   \
    GPRINT:sr_tempcpu:MAX:"Max\: %5.2lf °C"                              \
    GPRINT:sr_tempcpu:MIN:"Min\: %5.2lf °C\n"                            \
    LINE1:wr_tempcpu#ffcc00:"Temperatur Raspberry Pi Kleiderkasten    "  \
    GPRINT:wr_tempcpu:LAST:"\t Aktuell\: %5.2lf °C"                      \
    GPRINT:wr_tempcpu:AVERAGE:"Mittelwert\: %5.2lf °C"                   \
    GPRINT:wr_tempcpu:MAX:"Max\: %5.2lf °C"                              \
    GPRINT:wr_tempcpu:MIN:"Min\: %5.2lf °C\n"                            \
    LINE1:out_tempcpu#dcdcdc:"Temperatur NanoPi NEO Air Garten         " \
    GPRINT:out_tempcpu:LAST:"\t Aktuell\: %5.2lf °C"                     \
    GPRINT:out_tempcpu:AVERAGE:"Mittelwert\: %5.2lf °C"                  \
    GPRINT:out_tempcpu:MAX:"Max\: %5.2lf °C"                             \
    GPRINT:out_tempcpu:MIN:"Min\: %5.2lf °C\n"                           \
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
    GPRINT:kb_k_tcpu:MIN:"Min\: %5.2lf °C\n"                             \
    LINE1:po_tempcpu#BE25EB:"Temperatur NanoPi NEO Air Pool           "  \
    GPRINT:po_tempcpu:LAST:"\t Aktuell\: %5.2lf °C"                      \
    GPRINT:po_tempcpu:AVERAGE:"Mittelwert\: %5.2lf °C"                   \
    GPRINT:po_tempcpu:MAX:"Max\: %5.2lf °C"                              \
    GPRINT:po_tempcpu:MIN:"Min\: %5.2lf °C\n"
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
    DEF:humi_outdoor=$RRD_OUT:humi:AVERAGE                     \
    DEF:humi_indoor=$RRD_IN:humi:AVERAGE                       \
    DEF:ki_humi=$RRD_KI:ki_humi:AVERAGE                        \
    DEF:kidsroom_humi=$RRD_K:kidsroom_humi:AVERAGE             \
    DEF:wr_humi=$RRD_WR:wr_humi:AVERAGE                        \
    DEF:sr_humi=$RRD_SR:humi:AVERAGE                           \
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
    LINE1:ki_humi#C8FE2E:"Luftfeuchtigkeit Küche            "  \
    GPRINT:ki_humi:LAST:"\t Aktuell\: %5.2lf %%"               \
    GPRINT:ki_humi:AVERAGE:"Mittelwert\: %5.2lf %%"            \
    GPRINT:ki_humi:MAX:"Max\: %5.2lf %%"                       \
    GPRINT:ki_humi:MIN:"Min\: %5.2lf %%\n"                     \
    LINE1:kidsroom_humi#00ccff:"Luftfeuchtigkeit Kinderzimmer     " \
    GPRINT:kidsroom_humi:LAST:"\t Aktuell\: %5.2lf %%"         \
    GPRINT:kidsroom_humi:AVERAGE:"Mittelwert\: %5.2lf %%"      \
    GPRINT:kidsroom_humi:MAX:"Max\: %5.2lf %%"                 \
    GPRINT:kidsroom_humi:MIN:"Min\: %5.2lf %%\n"               \
    LINE1:wr_humi#ffcc00:"Luftfeuchtigkeit Kleiderkasten    "  \
    GPRINT:wr_humi:LAST:"\t Aktuell\: %5.2lf %%"               \
    GPRINT:wr_humi:AVERAGE:"Mittelwert\: %5.2lf %%"            \
    GPRINT:wr_humi:MAX:"Max\: %5.2lf %%"                       \
    GPRINT:wr_humi:MIN:"Min\: %5.2lf %%\n"                     \
    LINE1:sr_humi#000000:"Luftfeuchtigkeit Serverraum       "  \
    GPRINT:sr_humi:LAST:"\t Aktuell\: %5.2lf %%"               \
    GPRINT:sr_humi:AVERAGE:"Mittelwert\: %5.2lf %%"            \
    GPRINT:sr_humi:MAX:"Max\: %5.2lf %%"                       \
    GPRINT:sr_humi:MIN:"Min\: %5.2lf %%\n"                     \
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
    DEF:air_pressure=$RRD_IN:pressure:AVERAGE            \
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


#######################################################################
# printWardrobe()                                                     #
# Parameter:                                                          #
# $1 Time Range                                                       #
# $2 Filename                                                         #
#######################################################################
printWardrobe()
  {
    rrdtool graph $2                                     \
    --title "Kleiderkasten"                              \
    --end now --start end-$1                             \
    -w $WIDTH -h $(($HEIGHT/2)) -a PNG                   \
    --watermark "$WATERMARK"                             \
    --alt-y-grid                                         \
    --right-axis 1:0                                     \
    DEF:wr_open1=$RRD_WR:wr_open1:AVERAGE                \
    DEF:wr_open2=$RRD_WR:wr_open2:AVERAGE                \
    DEF:wr_open3=$RRD_WR:wr_open3:AVERAGE                \
    DEF:wr_open4=$RRD_WR:wr_open4:AVERAGE                \
    AREA:wr_open1#ffcc00:"Kleiderkasten offen  "         \
    GPRINT:wr_open1:LAST:"\t Aktuell\: %5.0lf"           \
    GPRINT:wr_open1:AVERAGE:"Mittelwert\: %5.2lf\n"      \
    STACK:wr_open3#ffff00:"Lade offen           "        \
    GPRINT:wr_open3:LAST:"\t Aktuell\: %5.0lf"           \
    GPRINT:wr_open3:AVERAGE:"Mittelwert\: %5.2lf\n"
 }


#######################################################################
# printAnteroom()                                                     #
# Parameter:                                                          #
# $1 Time Range                                                       #
# $2 Filename                                                         #
#######################################################################
printAnteroom()
  {
    rrdtool graph $2                                     \
    --title "Vorzimmer"                                  \
    --end now --start end-$1                             \
    -w $WIDTH -h $(($HEIGHT/2)) -a PNG                   \
    --watermark "$WATERMARK"                             \
    --alt-y-grid                                         \
    --right-axis 1:0                                     \
    DEF:ar_switch=$RRD_AR:ar_switch:AVERAGE              \
    AREA:ar_switch#ff1493:"Licht ein           "         \
    GPRINT:ar_switch:LAST:"\t Aktuell\: %5.0lf"          \
    GPRINT:ar_switch:AVERAGE:"Mittelwert\: %5.2lf\n"
 }


#######################################################################
# printLightness()                                                    #
# Parameter:                                                          #
# $1 Time Range                                                       #
# $2 Filename                                                         #
#######################################################################
printLightness()
  {
    rrdtool graph $2                                        \
    --title "Helligkeit [lux]"                              \
    --end now --start end-$1                                \
    -w $WIDTH -h $HEIGHT -a PNG                             \
    --alt-autoscale                                         \
    --alt-y-grid                                            \
    --rigid                                                 \
    --watermark "$WATERMARK"                                \
    --right-axis 1:0                                        \
    --right-axis-format "%4.0lf"                            \
    DEF:wr_lightness=$RRD_WR:wr_lightness:AVERAGE           \
    DEF:ki_lightness=$RRD_KI:ki_lightness:AVERAGE           \
    DEF:out_lightness=$RRD_OUT:lightness:AVERAGE            \
    LINE1:ki_lightness#C8FE2E:"Helligkeit Küche           " \
    GPRINT:ki_lightness:LAST:"\t Aktuell\: %5.2lf lux"      \
    GPRINT:ki_lightness:AVERAGE:"Mittelwert\: %5.2lf lux"   \
    GPRINT:ki_lightness:MAX:"Max\: %5.2lf lux"              \
    GPRINT:ki_lightness:MIN:"Min\: %5.2lf lux\n"            \
    LINE1:wr_lightness#ffcc00:"Helligkeit Kleiderkasten   " \
    GPRINT:wr_lightness:LAST:"\t Aktuell\: %5.2lf lux"      \
    GPRINT:wr_lightness:AVERAGE:"Mittelwert\: %5.2lf lux"   \
    GPRINT:wr_lightness:MAX:"Max\: %5.2lf lux"              \
    GPRINT:wr_lightness:MIN:"Min\: %5.2lf lux\n"            \
    LINE1:out_lightness#0000FF:"Helligkeit draußen         " \
    GPRINT:out_lightness:LAST:"\t Aktuell\: %5.2lf lux"     \
    GPRINT:out_lightness:AVERAGE:"Mittelwert\: %5.2lf lux"  \
    GPRINT:out_lightness:MAX:"Max\: %5.2lf lux"             \
    GPRINT:out_lightness:MIN:"Min\: %5.2lf lux\n"
 }


#######################################################################
# printAirQuality()                                                   #
# Parameter:                                                          #
# $1 Time Range                                                       #
# $2 Filename                                                         #
#######################################################################
printAirQuality()
  {
    rrdtool graph $2                                           \
    --title "Luftqualität [%]"                                 \
    --end now --start end-$1                                   \
    -w $WIDTH -h $HEIGHT -a PNG                                \
    --watermark "$WATERMARK"                                   \
    --right-axis 1:0                                           \
    DEF:in_airquality=$RRD_IN:airquality:AVERAGE               \
    DEF:ki_airquality=$RRD_KI:ki_airquality:AVERAGE            \
    DEF:kb_airquality=$RRD_KB:kb_i_airquality:AVERAGE          \
    LINE1:in_airquality#FF0000:"Luftqualität Wohnzimmer      " \
    GPRINT:in_airquality:LAST:"\t Aktuell\: %5.2lf %%"         \
    GPRINT:in_airquality:AVERAGE:"Mittelwert\: %5.2lf %%"      \
    GPRINT:in_airquality:MAX:"Max\: %5.2lf %%"                 \
    GPRINT:in_airquality:MIN:"Min\: %5.2lf %%\n"               \
    LINE1:ki_airquality#C8FE2E:"Luftqualität Küche           " \
    GPRINT:ki_airquality:LAST:"\t Aktuell\: %5.2lf %%"         \
    GPRINT:ki_airquality:AVERAGE:"Mittelwert\: %5.2lf %%"      \
    GPRINT:ki_airquality:MAX:"Max\: %5.2lf %%"                 \
    GPRINT:ki_airquality:MIN:"Min\: %5.2lf %%\n"               \
    LINE1:kb_airquality#40FF00:"Luftqualität Kollerberg      " \
    GPRINT:kb_airquality:LAST:"\t Aktuell\: %5.2lf %%"         \
    GPRINT:kb_airquality:AVERAGE:"Mittelwert\: %5.2lf %%"      \
    GPRINT:kb_airquality:MAX:"Max\: %5.2lf %%"                 \
    GPRINT:kb_airquality:MIN:"Min\: %5.2lf %%\n"
 }


#######################################################################
# main ################################################################
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

printAnteroom "36h", "$PNG_ANTEROOM_D"
printAnteroom "7d", "$PNG_ANTEROOM_W"
printAnteroom "30d", "$PNG_ANTEROOM_M"
printAnteroom "365d", "$PNG_ANTEROOM_Y"

printWardrobe "36h", "$PNG_WARDROBE_D"
printWardrobe "7d", "$PNG_WARDROBE_W"
printWardrobe "30d", "$PNG_WARDROBE_M"
printWardrobe "365d", "$PNG_WARDROBE_Y"

printLightness "36h", "$PNG_WR_LIGHTNESS_D"
printLightness "7d", "$PNG_WR_LIGHTNESS_W"
printLightness "30d", "$PNG_WR_LIGHTNESS_M"
printLightness "365d", "$PNG_WR_LIGHTNESS_Y"

printAirQuality "36h", "$PNG_AIRQUALITY_D"
printAirQuality "7d", "$PNG_AIRQUALITY_W"
printAirQuality "30d", "$PNG_AIRQUALITY_M"
printAirQuality "365d", "$PNG_AIRQUALITY_Y"

mv $PICS/*png $PICS_STORE

# eof #

