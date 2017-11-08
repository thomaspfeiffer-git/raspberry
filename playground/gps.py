#!/usr/bin/python3
############################################################################
# gps.py                                                                   #
# (c) Thomas Pfeiffer, 2017                                                #
############################################################################
"""testing adafruit's ultimate GPS
   https://learn.adafruit.com/adafruit-ultimate-gps-on-the-raspberry-pi/introduction
"""

# you might need to install:
# sudo apt-get install gpsd gpsd-clients python-gps -y

# howto start and test:
"""
sudo systemctl stop gpsd.socket
sudo systemctl disable gpsd.socket
sudo gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock

cgps -s
"""

import gps
import pprint

# Listen on port 2947 (gpsd) of localhost
session = gps.gps("localhost", "2947")
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

while True:
    try:
        report = session.next()
        # Wait for a 'TPV' report and display the current time
        # To see all report data, uncomment the line below
        # print report
        if report['class'] == 'TPV':
        #     if hasattr(report, 'time'):
        #         print report.time
            pprint.pprint(report)
    except KeyError:
        pass
    except KeyboardInterrupt:
        quit()
    except StopIteration:
        session = None
        print "GPSD has terminated"


# eof #

