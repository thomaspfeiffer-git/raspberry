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

from flask import Flask, render_template, request
app = Flask(__name__)


############################################################################
class Flags (Enum):
    running = 0
    pattern_changed = 1

class Colors (Enum):
    """html color codes"""
    red     = 0xFF0000
    green   = 0x00FF00
    blue    = 0x0000FF
    yellow  = 0xFFFF00
    fuchsia = 0xFF00FF
    aqua    = 0x00FFFF
    white   = 0xFFFFFF
    black   = 0x000000


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
def pattern_color (strip, flags, kwargs):
    strip.set_color(kwargs['color'])  # TODO: use constant instead of magic string
    while flags[Flags.running] and not flags[Flags.pattern_changed]:
        sleep(0.05) 


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

    delay = kwargs['delay'] # TODO: constant instead of magic string
    
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
def help():
    return render_template('documentation.html')


@app.route('/on')
def light_on ():
    return "not implemented yet"


@app.route('/off')
def light_off ():
    c.set_pattern(method=pattern_color, color=Colors.black.value)
    return "set off"


@app.route('/color/<color>')
def set_color (color):
    if color in Colors.__members__.keys():
        color = Colors[color].value 
        c.set_pattern(method=pattern_color, color=color)
        return "color set"
    else:
        return "unknown color"


@app.route('/colorrgb/<string:color>')
def set_color_rgb (color):
    return "Farbe RGB: {}".format(color)


@app.route('/rainbow')
def rainbow ():
    delay = int(request.args.get('delay', '5000'))  # delay in milliseconds
    c.set_pattern(method=pattern_rainbow, delay=delay)
    return "rainbow, delay: {}".format(delay)


@app.route('/lightness')
def lightness ():
    return "not implemented yet"


############################################################################
### main ###
### if __name__ == 'main': ÄÄÄÄÄÄÄÄ oder so?
# TODO: signal etc

c = Control_Strip()
c.set_pattern(method=pattern_color, color=Colors.red.value)
c.start()
# c.stop()
# c.join()

# eof #
