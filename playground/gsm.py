#!/usr/bin/python3 -u


"""
Documentation
=============

Status LED
----------

Blink every 1s: The module is running but hasn’t made connection to the cellular network yet.
Blink every 2s: The GPRS data connection you requested is active.
Blink every 3s: The module has made contact with the cellular network & can send/receive voice and SMS.
Source: https://lastminuteengineers.com/sim800l-gsm-module-arduino-tutorial/


Users/Groups
------------

sudo usermod -a -G dialout


Shell access
------------

$> screen /dev/ttyUSB0 115200


Send SMS
--------

AT
OK
AT+CMGF=1
OK
AT+CSMP=17,167,0,0
OK
AT+CMGS="0676xxxxxxx"
> hello world
+CMGS: 12

# don't forget to enter ctrl-z after the message text and before CR

OK


Further documentation
---------------------

https://elinux.org/RPi_Serial_Connection
http://g-heinrichs.de/attiny/module/SIM800L.pdf

"""



import serial
import os, time

# Enable Serial Communication
port = serial.Serial('/dev/ttyUSB0', baudrate=115200, timeout=60)

# Transmitting AT Commands to the Modem
# '\r\n' indicates the Enter key

# port.write(b'AT\r\n')
# port.write(b'AT+COPS?\r\n')
# port.write(b'AT+COPS=?\r\n')
port.write(b'AT+CUSD=1,"*101#"\r\n')
rcv = port.read(256)
print(rcv)



