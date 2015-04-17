#!/usr/bin/python

import smbus
import time


IODIRA = 0x00 # Pin direction register
IODIRB = 0x01 # Pin direction register
OLATA  = 0x14 # Register for outputs
OLATB  = 0x15 # Register for outputs

i2c_devices = [0x20, 0x21]


i2c = smbus.SMBus(1)





# Init
# Portexpander #1, Address 0x20
i2c.write_byte_data(0x20, 0x00, 0x00)
i2c.write_byte_data(0x20, 0x01, 0b00000000)


# Init
# Portexpander #2, Address 0x21
i2c.write_byte_data(0x21, 0x00, 0b00000000)
i2c.write_byte_data(0x21, 0x01, 0b00000000)


def AllOff():
   i2c.write_byte_data(0x20, 0x14, 0x00)   # GBAx
   i2c.write_byte_data(0x20, 0x15, 0x00)   # GBPx
   i2c.write_byte_data(0x21, 0x14, 0x00)   # GBAx
   i2c.write_byte_data(0x21, 0x15, 0x00)   # GBPx


AllOff()

i2c.write_byte_data(0x20, 0x14, 0x80)
read = i2c.read_byte_data(0x20,012)
print read
time.sleep(1)

i2c.write_byte_data(0x20, 0x14, 0x40)
time.sleep(1)
i2c.write_byte_data(0x20, 0x15, 0x01)
time.sleep(1)
i2c.write_byte_data(0x20, 0x15, 0x02)
time.sleep(1)
i2c.write_byte_data(0x21, 0x14, 0x80)
time.sleep(1)
i2c.write_byte_data(0x21, 0x15, 0x01)
time.sleep(1)


AllOff()


