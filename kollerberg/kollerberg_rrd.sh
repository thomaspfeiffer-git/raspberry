#/bin/bash

HEARTBEAT=180

rrdtool create weather_kollerberg.rrd --step 60 \
DS:kb_i_t1:GAUGE:$HEARTBEAT:-40:80 \
DS:kb_i_t2:GAUGE:$HEARTBEAT:-40:80 \
DS:kb_i_tcpu:GAUGE:$HEARTBEAT:-40:80 \
DS:kb_i_humi:GAUGE:$HEARTBEAT:0:125 \
DS:kb_i_press:GAUGE:$HEARTBEAT:900:1040 \
DS:kb_i_airquality:GAUGE:$HEARTBEAT:0:100 \
DS:kb_a_t1:GAUGE:$HEARTBEAT:-40:80 \
DS:kb_a_t2:GAUGE:$HEARTBEAT:-40:80 \
DS:kb_a_tcpu:GAUGE:$HEARTBEAT:-40:80 \
DS:kb_a_humi:GAUGE:$HEARTBEAT:0:125 \
DS:kb_a_press:GAUGE:$HEARTBEAT:900:1040 \
DS:kb_a_airquality:GAUGE:$HEARTBEAT:0:100 \
DS:kb_k_t1:GAUGE:$HEARTBEAT:-40:80 \
DS:kb_k_t2:GAUGE:$HEARTBEAT:-40:80 \
DS:kb_k_tcpu:GAUGE:$HEARTBEAT:-40:80 \
DS:kb_k_humi:GAUGE:$HEARTBEAT:0:125 \
DS:kb_k_press:GAUGE:$HEARTBEAT:900:1040 \
DS:kb_k_airquality:GAUGE:$HEARTBEAT:0:100 \
DS:kb_res1:GAUGE:$HEARTBEAT:-40:80 \
DS:kb_res2:GAUGE:$HEARTBEAT:-40:80 \
DS:kb_res3:GAUGE:$HEARTBEAT:-40:80 \
DS:kb_res4:GAUGE:$HEARTBEAT:-40:80 \
DS:kb_res5:GAUGE:$HEARTBEAT:-40:80 \
RRA:AVERAGE:0.5:1:7200 \
RRA:AVERAGE:0.5:5:4032 \
RRA:AVERAGE:0.5:60:744 \
RRA:AVERAGE:0.5:1440:3650 \

# 7200: 1440 Werte pro Tag x 5 Tage
# 4032: je fünf Werte (= fünf Minuten) = 12 Werte je Stunde = 288 Werte je Tag
#       = 4032 Werte für 14 Tage
# 744:  je 60 Werte (= 1 Stunde) für 31 Tage: = 24*31 = 744 Werte
# 3650: je 1440 Werte (=1 Tag) für 10 Jahre = 3650












