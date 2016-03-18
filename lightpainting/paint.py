#!/usr/bin/python
 
# Light painting / POV demo for Raspberry Pi using
# Adafruit Digital Addressable RGB LED flex strip.
# ----> http://adafruit.com/products/306 

import getopt 
# import Image
import RPi.GPIO as GPIO
import signal
import sys
import time


# Number of LEDs in the LED bar
LED_COUNT = 64

# Wait time until first iteration starts.
# Needed to move from camera to led strip. :-)
# Can be set using the command line paramter -s <time>.
DELAYTOSTART = 5.0

# Sleep time between columns. 
# Has to be adjusted according speed of LED bar.
# Can be set using the command line parameter -c <time>.
COLUMN_SLEEP  = 0.1

# Repeat display of picture. 
# Can be set using the command line parameter -l
PICTURE_REPEAT = False

# Sleep time between pictures (if PICTURE_REPEAT == True).
PICTURE_SLEEP  = 1.0


# filename = "images/testbild.png"
# filename = "images/wh_logo_64px_blackcyan.png"
# filename = "images/DonaldDuck.png"
# filename = "images/Minions.png"


dev = "/dev/spidev0.0"


def usage():
    print sys.argv[0], "-p <picture> -s <time> -c <time> -l"
    print "-p: path to picture in png format"
    print "-s: delay until start in seconds"
    print "-c: delay between columns in seconds"
    print "-l: looping forever"
    sys.exit()


def readCommandLine():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "p:s:c:l")
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        usage()

    picture = None
    delaytostart   = DELAYTOSTART
    column_sleep   = COLUMN_SLEEP
    picture_repeat = PICTURE_REPEAT    

    for o, a in opts:
        if o == "-p":
            picture = a
        elif o == "-s":
            delaytostart = float(a)
        elif o == "-c":
            column_sleep = float(a) 
        elif o == "-l":
            picture_repeat = True
        else:
            usage()
    if not picture:
        usage()

    print "Picture:", picture
    print "Delay to start:", delaytostart
    print "Column sleep:", column_sleep
    print "Picture repeat:", picture_repeat
    print ""

    return picture, delaytostart, column_sleep, picture_repeat


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


###############################################################################
# Exit ########################################################################
def Exit():
    """stuff to be done on exit"""
    blackColumn()
    sys.exit()

def _Exit(__s, __f):
    """exit for signal handler"""
    Exit()


###############################################################################
# Main ########################################################################
def Main():

    filename, delaytostart, column_sleep, picture_repeat = readCommandLine()
    spidev = file(dev, "wb")

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
    time.sleep(delaytostart)

    # Then it's a trivial matter of writing each column to the SPI port.
    print "Displaying ..."
    while True:
        for x in range(width):
            writeColumn(column[x])
            time.sleep(column_sleep)
            print "Looping %i for picture %s" % (x, filename)

        blackColumn()
        if not picture_repeat:
            break
        time.sleep(PICTURE_SLEEP)


###############################################################################
###############################################################################
if __name__ == '__main__':
    signal.signal(signal.SIGTERM, _Exit)

    try:
        Main()

    except KeyboardInterrupt:
        Exit()

    except SystemExit:              # Done in signal handler (method _Exit()) #
        pass

    except:
        print(traceback.print_exc())

    finally:    # All cleanup is done in KeyboardInterrupt or signal handler. #
        pass

# eof #

