#!/usr/bin/python3 -u

import pprint
pp = pprint.PrettyPrinter(indent=4)

import xml.dom.minidom

DT = xml.dom.minidom.parse("schedule.xml")
collection = DT.documentElement


schedules = collection.getElementsByTagName("schedule")
for sched in schedules:
    start = sched.getElementsByTagName('start')[0]
    print("start: {}".format(start.childNodes[0].data))


