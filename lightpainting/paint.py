#!/usr/bin/python
 
# Light painting / POV demo for Raspberry Pi using
# Adafruit Digital Addressable RGB LED flex strip.
# ----> http://adafruit.com/products/306 

import RPi.GPIO as GPIO, Image, time


LED_COUNT = 64

 
# Configurable values
filename = "images/testbild.png"
# filename  = "images/wh_logo_64px_blackcyan.png"
# filename  = "images/DonaldDuck.png"
# filename  = "images/minions.png"
dev       = "/dev/spidev0.0"
 
# Open SPI device, load image in RGB format and get dimensions:
spidev    = file(dev, "wb")

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
 
 
# Then it's a trivial matter of writing each column to the SPI port.
print "Displaying ..."
while True:
        for x in range(width):
                spidev.write(column[x])
                spidev.flush()
                time.sleep(0.1)
        time.sleep(0.5)



