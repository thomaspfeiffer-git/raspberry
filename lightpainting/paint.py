#!/usr/bin/python
 
# Light painting / POV demo for Raspberry Pi using
# Adafruit Digital Addressable RGB LED flex strip.
# ----> http://adafruit.com/products/306 

import getopt, sys
import RPi.GPIO as GPIO, Image, time

LED_COUNT = 64
DELAYTOSTART = 5.0

# Sleep time between columns. 
# Has to be adjusted according speed of LED bar.
COLUMN_SLEEP  = 0.1

# Repeat display of picture. 
# Mainly used for testing.
PICTURE_REPEAT = False

# Sleep time between pictures (if PICTURE_REPEAT == True).
PICTURE_SLEEP  = 1.0


# Configurable values
# filename = "images/testbild.png"
# filename = "images/wh_logo_64px_blackcyan.png"
# filename = "images/DonaldDuck.png"
# filename = "images/Minions.png"


dev = "/dev/spidev0.0"
spidev = file(dev, "wb")


def usage():
    print sys.argv[0], "-p <picture>"
    sys.exit()


def readCommandLine():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "p:")
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        usage()

    picture = None
    for o, a in opts:
        if o == "-p":
            picture = a
        else:
            usage()
    if not picture:
        usage()

    print "Picture: ", picture
    return picture


def writeColumn(column):
    """writes a column to the led strip"""
    spidev.write(column)
    spidev.flush()


def blackColumn():
    """method to black all LEDs"""
    print "Blacking ..."
    blackcolumn = bytearray(height * 3 + 1) # TODO: Calculate only once by using a closure
    for y in range(height):
        y3 = y * 3
        blackcolumn[y3]     = gamma[0]
        blackcolumn[y3 + 1] = gamma[0]
        blackcolumn[y3 + 2] = gamma[0]
    writeColumn(blackcolumn)



#### main ####

filename = readCommandLine()

print "Loading ..."
img     = Image.open(filename).convert("RGB")
img     = img.rotate(180)
width   = img.size[0]
height  = img.size[1]
print "   %dx%d pixels" % (width, height)


print "Resizing ..."
newWidth = float(img.size[0])/float(img.size[1])*LED_COUNT
img = img.resize( (int(newWidth), LED_COUNT))
width   = img.size[0]
height  = img.size[1]
pixels  = img.load()
print "   %dx%d pixels" % (width, height)

 
# Calculate gamma correction table.  This includes
# LPD8806-specific conversion (7-bit color w/high bit set).
print "Gamma correcting ..."
gamma = bytearray(256)
for i in range(256):
    gamma[i] = 0x80 | int(pow(float(i) / 255.0, 2.5) * 127.0 + 0.5)

 
# Create list of bytearrays, one for each column of image.
# R, G, B byte per pixel, plus extra '0' byte at end for latch.
print "Allocating ..."
column = [0 for x in range(width)]
for x in range(width):
    column[x] = bytearray(height * 3 + 1)

 
# Convert 8-bit RGB image into column-wise GRB bytearray list.
print "Converting ..."
for x in range(width):
    for y in range(height):
        value = pixels[x, y]
        y3 = y * 3
        column[x][y3]     = gamma[value[1]]
        column[x][y3 + 1] = gamma[value[0]]
        column[x][y3 + 2] = gamma[value[2]]
 

print "Waiting for start ..."
time.sleep(DELAYTOSTART)

# Then it's a trivial matter of writing each column to the SPI port.
print "Displaying ..."
while True:
    for x in range(width):
        writeColumn(column[x])
        time.sleep(COLUMN_SLEEP)
        print "Looping %i for picture %s" % (x, s)

    blackColumn()
    if not PICTURE_REPEAT:
        break
    time.sleep(PICTURE_SLEEP)

# eof #

