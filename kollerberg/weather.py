#!/usr/bin/python3

from socket import gethostname


# Hosts where this app runs
pik_i = "pik_i"
pik_a = "pik_a"
pik_k = "pik_k"
PIs = [pik_i, pik_a, pik_k]


# Datenstruktur fuer diverse Namen, zB in der rrd erstellen


this_PI = gethostname()

if this_PI not in PIs:
   print("falscher host!")
