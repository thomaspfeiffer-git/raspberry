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
#
# https://learn.adafruit.com/neopixels-on-raspberry-pi/software



from enum import Enum
from flask import Flask, request, Markup, render_template
from neopixel import *
from random import randrange
import signal
import sys
import threading
from time import sleep

from scheduling import Scheduling, Scheduling_Params
from userinterface import Feedback, Status

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
#    COUNT      = 288-13-13   # Number of LED pixels.
    COUNT      = 20
    PIN        = 18          # GPIO pin connected to the pixels
    FREQ_HZ    = 800000      # LED signal frequency in hertz (usually 800khz)
    DMA        = 5           # DMA channel to use for generating signal (try 5)
    BRIGHTNESS = 25          # Set to 0 for darkest and 255 for brightest
    INVERT     = False  

    def __init__ (self):
        """set_brighness() may interrupt set_color(). to avoid some
           sync crazyness, a lock is used.
        """
        self.__show_lock = threading.Lock()

    def set_brightness (self, brightness):
        with self.__show_lock:
            self._strip.setBrightness(brightness)
            self.show()

    def set_pixel_color (self, i, color):
        b = color & 255
        g = (color >> 8) & 255
        r = (color >> 16) & 255
        color = (g << 16) + (r << 8) + b
        self._strip.setPixelColor(i, color)

    def num_pixels (self):
        return self._strip.numPixels()

    def set_color (self, color):
        with self.__show_lock:
            for i in range(self.num_pixels()):
                self.set_pixel_color(i, color)
            self.show()

    def set_color_strip (self, colors):
        with self.__show_lock:
            for i, color in enumerate(colors):
                self.set_pixel_color(i, color)
            self.show()

    def begin (self):
        self.end()
        self._strip = Adafruit_NeoPixel(self.COUNT, self.PIN, self.FREQ_HZ, \
                                        self.DMA, self.INVERT, self.BRIGHTNESS)
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
    strip.set_color(kwargs['color'])
    while flags[Flags.running] and not flags[Flags.pattern_changed]:
        sleep(0.05) 


def pattern_random (strip, flags, kwargs):
    def random_color_strip ():
        def random_color ():
            return Color(randrange(0, 255), randrange(0, 255), randrange(0, 255))
        return [random_color() for i in range(strip.num_pixels())]

    delay = kwargs['delay']

    while flags[Flags.running] and not flags[Flags.pattern_changed]:
        strip.set_color_strip(random_color_strip())

        if not flags[Flags.running] or flags[Flags.pattern_changed]:
            break

        for s in range(delay):    # interruptible sleep  
            if flags[Flags.running] and not flags[Flags.pattern_changed]:
                sleep(0.001)


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

    delay = kwargs['delay']
    
    while flags[Flags.running] and not flags[Flags.pattern_changed]:
        for j in range(256):
            color = wheel(j)
            strip.set_color(color)

            if not flags[Flags.running] or flags[Flags.pattern_changed]:
               break

            for s in range(delay):    # interruptible sleep  
                if flags[Flags.running] and not flags[Flags.pattern_changed]:
                    sleep(0.001)


############################################################################
# Flask stuff ##############################################################
@app.route('/')
def help ():
    return render_template('documentation.html')


@app.route('/status')
def status ():
    return "{}".format(Feedback(status=status))


@app.route('/off')
def light_off (scheduler_off=True, on_exit=False):
    """Switches the LEDs off. When explicitely called by the scheduler,
       scheduler_off shall be set to False to not cancel the scheduling."""
    status.set(pattern="off")
    if scheduler_off:
        scheduler.cancel()

    control.set_pattern(method=pattern_color, color=Colors.black.value)

    if not on_exit:
        return "{}".format(Feedback(success="LEDs off", status=status))


@app.route('/color/<color>')
def set_color (color):
    """sets LEDs to a static color"""
    if color in Colors.__members__.keys():
        if not scheduling_params.get_scheduling_params(request.args):
            f = Feedback(error="format error!", status=status)
        else:
            status.set(pattern="color", color=color)
            status.schedule = scheduling_params

            scheduler.set_timings(scheduling_params)
            scheduler.set_method_on(method=pattern_color, \
                                    color=Colors[color].value)

            f = Feedback(success="color set to {}".format(color), \
                         status=status)
    else:
        f = Feedback(error="unknown color", status=status)
    return "{}".format(f)


@app.route('/rainbow')
def rainbow ():
    """sets LEDs to rainbow colors; 
       color is changed every <delay> milliseconds"""
    delay = int(request.args.get('delay', '5000'))  # delay in milliseconds
    if not scheduling_params.get_scheduling_params(request.args):
        f = Feedback(error="format error", status=status)
    else:
        status.set(pattern="rainbow", delay=delay)
        status.schedule = scheduling_params

        scheduler.set_timings(scheduling_params)
        scheduler.set_method_on(method=pattern_rainbow, delay=delay)
        f = Feedback(success="rainbow set", status=status)
    return "{}".format(f)


@app.route('/random')
def random ():
    """sets LEDs to random colors;
       color is changed every <delay> milliseconds"""

    delay = int(request.args.get('delay', '5000'))  # delay in milliseconds
    if not scheduling_params.get_scheduling_params(request.args):
        f = Feedback(error="format error", status=status)
    else:
        status.set(pattern="random", delay=delay)
        status.schedule = scheduling_params

        scheduler.set_timings(scheduling_params)
        scheduler.set_method_on(method=pattern_random, delay=delay)
        f = Feedback(success="random set", status=status)
    return "{}".format(f)


@app.route('/brightness/<int:brightness>')
def brightness (brightness):
    """sets brightness of LEDs; 0 .. 255"""
    try:
        control.brightness = brightness
        status.brightness  = brightness
    except ValueError:
        return "{}".format(Feedback(error="brightness has to be in 0 .. 255", \
                                    status=status))

    return "{}".format(Feedback(success="brightness set", status=status))


###############################################################################
# Exit ########################################################################
def _exit():
    """cleanup stuff"""
    light_off(scheduler_off=True, on_exit=True)
    sleep(0.5)  # give some time to switch off LEDs before threads are stopped
    control.stop()
    control.join()
    scheduler.stop()
    scheduler.join()
    sys.exit()

def __exit(__s, __f):
    """cleanup stuff used for signal handler"""
    _exit()


###############################################################################
# main ########################################################################
signal.signal(signal.SIGTERM, __exit)
signal.signal(signal.SIGINT, __exit)

status = Status(brightness=LED_Strip.BRIGHTNESS)

control = Control_Strip()
control.set_pattern(method=pattern_color, color=Colors.green.value)

scheduling_params = Scheduling_Params()

scheduler = Scheduling()
scheduler.set_pattern_method(control.set_pattern)
scheduler.set_method_off(method=pattern_color, color=Colors.black.value)
scheduler.set_logging_method(status.loginfo)

scheduler.start()
control.start()

# eof #

