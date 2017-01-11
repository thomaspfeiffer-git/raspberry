# -*- coding: utf-8 -*-
###############################################################################
# ssd1306.py                                                                  #
# Control of OLED Display SSD1306 (128 x 64)                                  #
# (c) https://github.com/thomaspfeiffer-git 2016, 2017                        #
###############################################################################
"""provides a class for handling the oled display SSD1306 (128 x 64)"""

# Source code taken and modified from
# https://github.com/adafruit/Adafruit_Python_SSD1306 
#
# Link to Amazon:
# https://www.amazon.de/Zoll-serielle-OLED-Display-Modul-Arduino/dp/B00NHKM1C0
# 
# Additional information:
# https://www.raspberrypi.org/forums/viewtopic.php?f=44&t=105635
# https://github.com/rm-hull/ssd1306 (fonts!)


from time import sleep
import sys
sys.path.append('../libs')
from i2c import I2C


class SSD1306 (I2C):
    # Constants
    I2C_ADDRESS = 0x3C    # 011110+SA0+RW - 0x3C or 0x3D
    SETCONTRAST = 0x81
    DISPLAYALLON_RESUME = 0xA4
    DISPLAYALLON = 0xA5
    NORMALDISPLAY = 0xA6
    INVERTDISPLAY = 0xA7
    DISPLAYOFF = 0xAE
    DISPLAYON = 0xAF
    SETDISPLAYOFFSET = 0xD3
    SETCOMPINS = 0xDA
    SETVCOMDETECT = 0xDB
    SETDISPLAYCLOCKDIV = 0xD5
    SETPRECHARGE = 0xD9
    SETMULTIPLEX = 0xA8
    SETLOWCOLUMN = 0x00
    SETHIGHCOLUMN = 0x10
    SETSTARTLINE = 0x40
    MEMORYMODE = 0x20
    COLUMNADDR = 0x21
    PAGEADDR = 0x22
    COMSCANINC = 0xC0
    COMSCANDEC = 0xC8
    SEGREMAP = 0xA0
    CHARGEPUMP = 0x8D
    EXTERNALVCC = 0x1
    SWITCHCAPVCC = 0x2

    # Scrolling constants
    ACTIVATE_SCROLL = 0x2F
    DEACTIVATE_SCROLL = 0x2E
    SET_VERTICAL_SCROLL_AREA = 0xA3
    RIGHT_HORIZONTAL_SCROLL = 0x26
    LEFT_HORIZONTAL_SCROLL = 0x27
    VERTICAL_AND_RIGHT_HORIZONTAL_SCROLL = 0x29
    VERTICAL_AND_LEFT_HORIZONTAL_SCROLL = 0x2A

    def __init__ (self, width=128, height=64, lock=None):
        if sys.version_info >= (3,0):
            super().__init__(lock)
        else:
            super(SSD1306, self).__init__(lock)

        self._address = SSD1306.I2C_ADDRESS
        self.width = width
        self.height = height
        self.__pages = height//8
        self.__buffer = [0]*(width*self.__pages)


    def __initialize (self):
        self.__command(SSD1306.DISPLAYOFF)                    # 0xAE
        self.__command(SSD1306.SETDISPLAYCLOCKDIV)            # 0xD5
        self.__command(0x80)                                  # the suggested ratio 0x80
        self.__command(SSD1306.SETMULTIPLEX)                  # 0xA8
        self.__command(0x3F)
        self.__command(SSD1306.SETDISPLAYOFFSET)              # 0xD3
        self.__command(0x0)                                   # no offset
        self.__command(SSD1306.SETSTARTLINE | 0x0)            # line #0
        self.__command(SSD1306.CHARGEPUMP)                    # 0x8D
        self.__command(0x14)
        self.__command(SSD1306.MEMORYMODE)                    # 0x20
        self.__command(0x00)                                  # 0x0 act like ks0108
        self.__command(SSD1306.SEGREMAP | 0x1)
        self.__command(SSD1306.COMSCANDEC)
        self.__command(SSD1306.SETCOMPINS)                    # 0xDA
        self.__command(0x12)
        #####################################   methode verwenden
        self.__command(SSD1306.SETCONTRAST)                   # 0x81
        self.__command(0x9F)
        self.__command(SSD1306.SETPRECHARGE)                  # 0xd9
        self.__command(0x22)
        self.__command(SSD1306.SETVCOMDETECT)                 # 0xDB
        self.__command(0x40)
        self.__command(SSD1306.DISPLAYALLON_RESUME)           # 0xA4
        self.__command(SSD1306.NORMALDISPLAY)                 # 0xA6


    def __command (self, c):
        """Send command byte to display."""
        retry = 0
        max_retries = 5
        control = 0x00   # Co = 0, DC = 0

        while retry < max_retries:
            try:
                I2C._bus.write_byte_data(self._address, control, c)
            except (IOError, OSError):
                print(strftime("%Y%m%d %X:"), "error writing i2c bus in SSD1306.__command()i; retry #", retry)
                sleep(0.5)
                retry += 1
        if retry >= max_retries:
            sys.exit()
                

#    def __data (self, c):
#        """Send byte of data to display."""
#        # I2C write.
#        control = 0x40   # Co = 0, DC = 0
#        I2C._bus.write_byte_data(self._address, control, c)


    def begin (self):
        """Initialize display."""
        self.clear()
        self.__initialize()
        self.__command(SSD1306.DISPLAYON)
        

    def display(self):
        """Write display buffer to physical display."""
        self.__command(SSD1306.COLUMNADDR)
        self.__command(0)              # Column start address. (0 = reset)
        self.__command(self.width-1)   # Column end address.
        self.__command(SSD1306.PAGEADDR)
        self.__command(0)              # Page start address. (0 = reset)
        self.__command(self.__pages-1) # Page end address.
        control = 0x40   # Co = 0, DC = 0
        for i in range(0, len(self.__buffer), 16):
            try:
                I2C._bus.write_i2c_block_data(self._address, control, self.__buffer[i:i+16])
            except (IOError, OSError):
                # continue with next line on exception.
                # this might lead to some broken images but will kind
                # of self repair with the next call of display().
                # maybe TODO: full new display()
                print(strftime("%Y%m%d %X:"), "error writing i2c bus in SSD1306.display(), displaying line", i)


    def image (self, image):
        """Set buffer to value of Python Imaging Library image.  The image should
        be in 1 bit mode and a size equal to the display size.
        """
        if image.mode != '1':
            raise ValueError('Image must be in mode 1.')
        imwidth, imheight = image.size
        if imwidth != self.width or imheight != self.height:
            raise ValueError('Image must be same dimensions as display ({0}x{1}).' \
                .format(self.width, self.height))
        # Grab all the pixels from the image, faster than getpixel.
        pix = image.load()
        # Iterate through the memory pages
        index = 0
        for page in range(self.__pages):
            # Iterate through all x axis columns.
            for x in range(self.width):
                # Set the bits for the column of pixels at the current position.
                bits = 0
                # Don't use range here as it's a bit slow
                for bit in [0, 1, 2, 3, 4, 5, 6, 7]:
                    bits = bits << 1
                    bits |= 0 if pix[(x, page*8+7-bit)] == 0 else 1
                # Update buffer byte and increment to next byte.
                self.__buffer[index] = bits
                index += 1


    def clear (self):
        """Clear contents of image buffer."""
        self.__buffer = [0]*(self.width*self.__pages)


    def set_contrast (self, contrast):
        """Sets the contrast of the display.  Contrast should be a value between
        0 and 255."""
        if contrast < 0 or contrast > 255:
            raise ValueError('Contrast must be a value from 0 to 255 (inclusive).')
        self.__command(SSD1306.SETCONTRAST)
        self.__command(contrast)

# eof #

