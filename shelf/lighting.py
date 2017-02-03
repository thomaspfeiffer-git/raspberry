#!/usr/bin/python3


### usage ###
# sudo bash
# export FLASK_APP=lighting.py
# flask run --host=0.0.0.0


# sudo PYTHONPATH=".:build/lib.linux-armv7l-2.7" python tp/strandtest.py &

### setup ###
# http://flask.pocoo.org/docs/0.12/
#
# http://jinja.pocoo.org/docs/2.9/
# sudo pip3 install Jinja2
#
# http://werkzeug.pocoo.org/docs/0.11/
# sudo pip3 install Werkzeug
#
# http://flask.pocoo.org/docs/0.12/
# sudo pip3 install Flask


from neopixel import *
import sys
import threading
from time import sleep

from flask import Flask
app = Flask(__name__)




############################################################################
# LED_Strip ################################################################
class LED_Strip (object):
    COUNT      = 288     # Number of LED pixels.
    PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
    FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
    DMA        = 5       # DMA channel to use for generating signal (try 5)
    BRIGHTNESS = 20      # Set to 0 for darkest and 255 for brightest
    INVERT     = False  

    def __init__ (self):
        self.__brightness = self.BRIGHTNESS

    def set_brightness (self, brightness):
        self.__brightness = brightness
        self.begin()

    def set_pixel_color (self, i, color):
        b = color & 255
        g = (color >> 8) & 255
        r = (color >> 16) & 255
        color = (g << 16) + (r << 8) + b
        self._strip.setPixelColor(i, color)

    def num_pixels (self):
        return self._strip.numPixels()

    def set_color (self, color):
        print("Control_Strip.set_color(): {}".format(color))
        for i in range(self.num_pixels()):
            self.set_pixel_color(i, color)
        self.show()

    def begin (self):
        self.end()
        self._strip = Adafruit_NeoPixel(self.COUNT, self.PIN, self.FREQ_HZ, \
                                        self.DMA, self.INVERT, \
                                        self.__brightness)
        self._strip.begin()

    def show (self):
        self._strip.show()

    def end (self):
        pass


############################################################################
# Control_Strip ############################################################
class Control_Strip (threading.Thread):
    def __init__ (self):
        threading.Thread.__init__(self)
        self._strip = LED_Strip()
        self._strip.begin()

        self.__running = [True]  # pass by reference in self.__pattern()
        self.__pattern_changed = [False]

    @property
    def brightness (self):
        raise NotImplementedError()

    @brightness.setter
    def brightness (self, value):
        if not 0 <= value <= 255:
            raise ValueError("'value' has to be in 0 .. 255")
        self._strip.set_brightness(value)

    def set_pattern (self, pattern):
        self.__pattern = pattern
        self.__pattern_changed[0] = True

    def run (self):
        self.__pattern_changed[0] = False
        while self.__running[0]:
            self.__pattern(self._strip, self.__running, self.__pattern_changed)
            self.__pattern_changed[0] = False
       
    def stop (self):
        self.__running[0] = False


############################################################################
# Patterns for LED Strip ###################################################
def pattern_red (strip, running, pattern_changed):
    strip.set_color(0xFF0000)
    while running[0] and pattern_changed[0] == False:
        sleep(1) 

def pattern_green (strip, running, pattern_changed):
    strip.set_color(0x00FF00)
    while running[0] and pattern_changed[0] == False:
        sleep(1) 

def pattern_blue (strip, running, pattern_changed):
    strip.set_color(0x0000FF)
    while running[0] and pattern_changed[0] == False:
        sleep(1) 

def pattern_yellow (strip, running, pattern_changed):
    strip.set_color(0xFFFF00)
    while running[0] and pattern_changed[0] == False:
        sleep(1) 

def pattern_fuchsia (strip, running, pattern_changed):
    strip.set_color(0xFF00FF)
    while running[0] and pattern_changed[0] == False:
        sleep(1) 

def pattern_aqua (strip, running, pattern_changed):
    strip.set_color(0x00FFFF)
    while running[0] and pattern_changed[0] == False:
        sleep(1) 

def pattern_white (strip, running, pattern_changed):
    strip.set_color(0xFFFFFF)
    while running[0] and pattern_changed[0] == False:
        sleep(1) 

def pattern_black (strip, running, pattern_changed):
    strip.set_color(0x000000)
    while running[0] and pattern_changed[0] == False:
        sleep(1) 


############################################################################
# Flask stuff ##############################################################
@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/on')
def light_on ():
    pass


@app.route('/off')
def light_off ():
    c.set_pattern(pattern_black)


@app.route('/color/red')
def set_color_red ():
    c.set_pattern(pattern_red)
    return "color set"

@app.route('/color/green')
def set_color_green ():
    c.set_pattern(pattern_green)
    return "color set"

@app.route('/color/blue')
def set_color_blue ():
    c.set_pattern(pattern_blue)
    return "color set"

@app.route('/color/yellow')
def set_color_yellow ():
    c.set_pattern(pattern_yellow)
    return "color set"

@app.route('/color/fuchsia')
def set_color_fuchsia ():
    c.set_pattern(pattern_fuchsia)
    return "color set"

@app.route('/color/aqua')
def set_color_aqua ():
    c.set_pattern(pattern_aqua)
    return "color set"


@app.route('/colorrgb/<string:color>')
def set_color_rgb (color):
    return "Farbe RGB: {}".format(color)


@app.route('/lightness')
def lightness ():
    pass


############################################################################
### main ###
### if __name__ == 'main': ÄÄÄÄÄÄÄÄ oder so?

c = Control_Strip()
c.set_pattern(pattern_red)
c.start()
# sleep(5)
# c.set_pattern(pattern_green)
# sleep(5)
# c.set_pattern(pattern_blue)
# sleep(5)
# c.set_pattern(pattern_white)
# sleep(5)
# c.set_pattern(pattern_black)
# sleep(5)
# c.stop()


# eof #

