#!/usr/bin/python3 -u



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



