################################################################################
# MCP23x17                                                                     #
# PINs for MCP23x17 components                                                 #
# Use with io.setmode(io.BOARD)                                                #
# (c) https://github.com/thomaspfeiffer-git May 2015                           #
################################################################################
"""PINs for MCP23x17 components"""

class MCP23x17:
    IODIRA      = 0x00 # Pin direction register
    IODIRB      = 0x01 # Pin direction register
    IOCONA      = 0x0A # MCP23S17 needs hardware addressing explicitly enabled.
    IOCONB      = 0x0B # MCP23S17 needs hardware addressing explicitly enabled.
    OLATA       = 0x14 # Register for outputs
    OLATB       = 0x15 # Register for outputs

    HAEN        = 0b00001000


### eof ###

