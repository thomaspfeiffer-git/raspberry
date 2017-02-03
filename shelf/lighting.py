#!/usr/bin/python3
# -*- coding: utf-8 -*-
############################################################################
# lighting.py                                                              #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2017                #
############################################################################
"""control lighting of our shelf"""


### usage ###
# sudo bash
# export FLASK_APP=lighting.py
# flask run --host=0.0.0.0


# sudo PYTHONPATH=".:build/lib.linux-armv7l-2.7" python tp/strandtest.py &

# >>> from flask import Markup
# >>> Markup('<strong>Hello %s!</strong>') % '<blink>hacker</blink>'
# Markup(u'<strong>Hello &lt;blink&gt;hacker&lt;/blink&gt;!</strong>')
# >>> Markup.escape('<blink>hacker</blink>')
# Markup(u'&lt;blink&gt;hacker&lt;/blink&gt;')
# >>> Markup('<em>Marked up</em> &raquo; HTML').striptags()
# u'Marked up \xbb HTML'




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


from enum import Enum
from neopixel import *
import sys
import threading
from time import sleep

from flask import Flask, request
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
        for i in range(self.num_pixels()):
            self.set_pixel_color(i, color)
        self.show()

    def begin (self):
        self.end()
        self._strip = Adafruit_NeoPixel(self.COUNT, self.PIN, self.FREQ_HZ, \
                                        self.DMA, self.INVERT, self.__brightness)
        self._strip.begin()

    def show (self):
        self._strip.show()

    def end (self):
        pass


############################################################################
class Flags (Enum):
    running = 0
    pattern_changed = 1


############################################################################
# Control_Strip ############################################################
class Control_Strip (threading.Thread):
    def __init__ (self):
        threading.Thread.__init__(self)
        self._strip = LED_Strip()
        self._strip.begin()
        self.__flags = {Flags.running: True, Flags.pattern_changed: False}

    @property
    def brightness (self):
        raise NotImplementedError()

    @brightness.setter
    def brightness (self, value):
        if not 0 <= value <= 255:
            raise ValueError("'value' has to be in 0 .. 255")
        self._strip.set_brightness(value)

    def set_pattern (self, method, **kwargs):
        self.__pattern = method
        self.__kwargs  = kwargs
        self.__flags[Flags.pattern_changed] = True

    def run (self):
        self.__flags[Flags.pattern_changed] = False
        while self.__flags[Flags.running]:
            self.__pattern(self._strip, self.__flags, self.__kwargs)
            self.__flags[Flags.pattern_changed] = False
       
    def stop (self):
        self.__flags[Flags.running] = False


############################################################################
# Patterns for LED Strip ###################################################
def static_pattern_wait (flags):
    while flags[Flags.running] and not flags[Flags.pattern_changed]:
        sleep(0.05) 

def pattern_red (strip, flags, kwargs):
    strip.set_color(0xFF0000)
    static_pattern_wait(flags)

def pattern_green (strip, flags, kwargs):
    strip.set_color(0x00FF00)
    static_pattern_wait(flags)

def pattern_blue (strip, flags, kwargs):
    strip.set_color(0x0000FF)
    static_pattern_wait(flags)

def pattern_yellow (strip, flags, kwargs):
    strip.set_color(0xFFFF00)
    static_pattern_wait(flags)

def pattern_fuchsia (strip, flags, kwargs):
    strip.set_color(0xFF00FF)
    static_pattern_wait(flags)

def pattern_aqua (strip, flags, kwargs):
    strip.set_color(0x00FFFF)
    static_pattern_wait(flags)

def pattern_white (strip, flags, kwargs):
    strip.set_color(0xFFFFFF)
    static_pattern_wait(flags)

def pattern_black (strip, flags, kwargs):
    strip.set_color(0x000000)
    static_pattern_wait(flags)


def pattern_rainbow (strip, flags, kwargs):
    def wheel (pos):
        if pos < 85:
            return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Color(0, pos * 3, 255 - pos * 3)

    delay = int(kwargs['delay']) # TODO: constant instant of magic string
    
    while flags[Flags.running] and not flags[Flags.pattern_changed]:
        for j in range(256):
            color = wheel(j)
            for i in range(strip.num_pixels()):
                strip.set_pixel_color(i, color)
            strip.show()

            if not flags[Flags.running] or flags[Flags.pattern_changed]:
               break

            for s in range(delay):    # interruptible sleep  
                if flags[Flags.running] and not flags[Flags.pattern_changed]:
                    sleep(0.001)


############################################################################
# Flask stuff ##############################################################
@app.route('/')
def hello_world():
    return "http://pia:5000/color/red"


@app.route('/on')
def light_on ():
    pass


@app.route('/off')
def light_off ():
    c.set_pattern(method=pattern_black)

@app.route('/color/red')
def set_color_red ():
    c.set_pattern(method=pattern_red)
    return "color set"

@app.route('/color/green')
def set_color_green ():
    c.set_pattern(method=pattern_green)
    return "color set"

@app.route('/color/blue')
def set_color_blue ():
    c.set_pattern(method=pattern_blue)
    return "color set"

@app.route('/color/yellow')
def set_color_yellow ():
    c.set_pattern(method=pattern_yellow)
    return "color set"

@app.route('/color/fuchsia')
def set_color_fuchsia ():
    c.set_pattern(method=pattern_fuchsia)
    return "color set"

@app.route('/color/aqua')
def set_color_aqua ():
    c.set_pattern(method=pattern_aqua)
    return "color set"

@app.route('/colorrgb/<string:color>')
def set_color_rgb (color):
    return "Farbe RGB: {}".format(color)


@app.route('/rainbow')
def rainbow ():
    delay = request.args.get('delay', '5000')  # delay in milliseconds
    c.set_pattern(method=pattern_rainbow, delay=delay)
    return "rainbow, delay: {}".format(delay)


@app.route('/lightness')
def lightness ():
    pass


############################################################################
### main ###
### if __name__ == 'main': ÄÄÄÄÄÄÄÄ oder so?
# TODO: signal etc

c = Control_Strip()
c.set_pattern(pattern_red)
c.start()
# c.stop()
# c.join()

# eof #

