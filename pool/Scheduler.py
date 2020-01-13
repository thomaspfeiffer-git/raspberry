#!/usr/bin/python3 -u



# install
# sudo pip3 install xmltodict

import xmltodict

import pprint
pp = pprint.PrettyPrinter(indent=2)


with open('schedule.xml') as fd:
    doc = xmltodict.parse(fd.read())
    pp.pprint(doc)


for s in doc['schedules']['schedule']:
    start = s['start']
    stop  = s['stop']
    print(f"start: {start}; stop: {stop}")

    if 'conditions' in s:
        for c in s['conditions']:
            print(f"c: {c}")

 # eof #

