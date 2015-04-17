#!/usr/bin/python

import smbus
import time

i2c = smbus.SMBus(1)


# Init
# Portexpander #1, Address 0x20
i2c.write_byte_data(0x20, 0x00, 0x00)
i2c.write_byte_data(0x20, 0x01, 0b00000000)


# Init
# Portexpander #2, Address 0x21
i2c.write_byte_data(0x21, 0x00, 0b00000000)
i2c.write_byte_data(0x21, 0x01, 0b00000000)






