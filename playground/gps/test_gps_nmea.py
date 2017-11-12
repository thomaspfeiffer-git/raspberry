#!/usr/bin/env python3



from gps3 import agps3 
import time



gpsd_socket = agps3.GPSDSocket()
gpsd_socket.connect()
gpsd_socket.watch()
data_stream = agps3.DataStream()


gpsd_socket.watch(enable=False, gpsd_protocol='json')
gpsd_socket.watch(gpsd_protocol='nmea')

for new_data in gpsd_socket:
    if new_data:
        print(gpsd_socket.response.strip())
    else:
        time.sleep(0.1) 

# eof #

