#!/usr/bin/python
# -*- coding: utf-8 -*-
#############################################################################
# kollerberg_to_rrd.py                                                      #
# (c) https://github.com/thomaspfeiffer-git 2016                            #
#############################################################################
"""converts data from Kollerberg data files into rrd"""

import rrdtool

# Hosts where data comes from.
pik_i = "pik_i"
pik_a = "pik_a"
pik_k = "pik_k"
PIs = [pik_i, pik_a, pik_k]

DATAFILES = { pik_i: "/schild/weather/kb_i_weather.data",
              pik_a: "/schild/weather/kb_a_weather.data",
              pik_k: "/schild/weather/kb_k_weather.data" }
RRDFILE    = "/schild/weather/weather_kollerberg.rrd"

DS_TEMP1 = "DS_TEMP1"
DS_TEMP2 = "DS_TEMP2"
DS_TCPU  = "DS_TCPU"
DS_HUMI  = "DS_HUMI"
DS_PRESS = "DS_PRESS"
DS = { pik_i: { DS_TEMP1: 'kb_i_t1', 
                DS_TEMP2: 'kb_i_t2',
                DS_TCPU : 'kb_i_tcpu',
                DS_HUMI : 'kb_i_humi',
                DS_PRESS: 'kb_i_press' },
       pik_a: { DS_TEMP1: 'kb_a_t1',
                DS_TEMP2: 'kb_a_t2',
                DS_TCPU : 'kb_a_tcpu',
                DS_HUMI : 'kb_a_humi',
                DS_PRESS: 'kb_a_press' },
       pik_k: { DS_TEMP1: 'kb_k_t1',
                DS_TEMP2: 'kb_k_t2',
                DS_TCPU : 'kb_k_tcpu',
                DS_HUMI : 'kb_k_humi',
                DS_PRESS: 'kb_k_press' }
     } 


rrd_template = ""
rrd_data = "N:"

for pi in PIs:
    with open (DATAFILES[pi], 'r') as f:
        rrd_template = rrd_template + DS[pi][DS_TEMP1] + ":" + \
                                      DS[pi][DS_TEMP2] + ":" + \
                                      DS[pi][DS_TCPU]  + ":" + \
                                      DS[pi][DS_HUMI]  + ":" + \
                                      DS[pi][DS_PRESS] + ":"
        rrd_data = rrd_data + f.read().split(":N:")[1].rstrip() + ":"
rrd_template = rrd_template.rstrip(":")
rrd_data     = rrd_data.rstrip(":")

# print rrd_template
# print rrd_data

rrdtool.update(RRDFILE, "--template", rrd_template, rrd_data) 


