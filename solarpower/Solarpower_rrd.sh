#/bin/bash

HEARTBEAT=180

rrdtool create solar.rrd --step 60 \
DS:Main_U_L1:GAUGE:$HEARTBEAT:-400:400 \
DS:Main_U_L2:GAUGE:$HEARTBEAT:-400:400 \
DS:Main_U_L3:GAUGE:$HEARTBEAT:-400:400 \
DS:Main_I_L1:GAUGE:$HEARTBEAT:-32:32 \
DS:Main_I_L2:GAUGE:$HEARTBEAT:-32:32 \
DS:Main_I_L3:GAUGE:$HEARTBEAT:-32:32 \
DS:Main_I_N:GAUGE:$HEARTBEAT:-32:32 \
DS:Main_I_tot:GAUGE:$HEARTBEAT:-32:32 \
DS:Main_P:GAUGE:$HEARTBEAT:-32000:32000 \
DS:Solar_U:GAUGE:$HEARTBEAT:-400:400 \
DS:Solar_I:GAUGE:$HEARTBEAT:-32:32 \
DS:Solar_P:GAUGE:$HEARTBEAT:-32000:32000 \
RRA:AVERAGE:0.5:1:7200 \
RRA:AVERAGE:0.5:5:4032 \
RRA:AVERAGE:0.5:60:744 \
RRA:AVERAGE:0.5:1440:3650 \

# 7200: 1440 Werte pro Tag x 5 Tage
# 4032: je fünf Werte (= fünf Minuten) = 12 Werte je Stunde = 288 Werte je Tag
#       = 4032 Werte für 14 Tage
# 744:  je 60 Werte (= 1 Stunde) für 31 Tage: = 24*31 = 744 Werte
# 3650: je 1440 Werte (=1 Tag) für 10 Jahre = 3650

