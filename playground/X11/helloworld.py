#!/usr/bin/python3
"""playground for pygame and a cool weather station"""

import os
import pygame
from pygame.locals import QUIT
import re
import signal
import sys
from time import strftime, localtime, time
import traceback


os.environ["SDL_FBDEV"] = "/dev/fb1"
os.environ['SDL_VIDEO_CENTERED'] = '1'



class CONFIG:
    """various config stuff"""
    WIDTH          = 320 # Screen resolution
    HEIGHT         = 480

    FONTSIZE       = int(HEIGHT / 8)
    FONTSIZE_SMALL = int(FONTSIZE / 2.4)
    FONTSIZE_TINY  = int(FONTSIZE / 3.4)

    MARGIN         = 3                 # Margin (pixels) from border
    SEP_Y          = int(FONTSIZE / 5) # Pixels between different elements

    class COLORS:
        """definitions of colors"""
        BACKGROUND = (255, 255, 255)
        DATE       = (0, 0, 0)
        DESC       = (0, 0, 0)
        SEP        = (0, 0, 0)
        INDOOR     = (255, 0, 0)
        OUTDOOR    = (0, 0, 255)
        KIDSROOM   = (0, 0xCC, 0xFF)
        TURTLE     = (0x08, 0x8A, 0x08)

    TIMETOFALLBACK = 10 # Wait 10 seconds until fallback to main screen


class CONSTANTS:
    """constant strings"""
    DAYOFWEEK = {'0': 'Sonntag',    \
                 '1': 'Montag',     \
                 '2': 'Dienstag',   \
                 '3': 'Mittwoch',   \
                 '4': 'Donnerstag', \
                 '5': 'Freitag',    \
                 '6': 'Samstag'}



###############################################################################
# Exit ########################################################################
def Exit():
    """stuff to be done on exit"""
    print("Exit")
    pygame.quit()
    sys.exit()

def _Exit(__s, __f):
    """exit for signal handler"""
    print("_Exit")
    Exit()


###############################################################################
###############################################################################
class Display (object):
    """all about displaying the various weather values on several screens"""
    def __init__ (self):
        self.screen = pygame.display.set_mode((CONFIG.WIDTH, CONFIG.HEIGHT), \
                                               pygame.NOFRAME)
        self.screen.fill(CONFIG.COLORS.BACKGROUND)

        self.font            = pygame.font.SysFont('arial', \
                                                   CONFIG.FONTSIZE)
        self.font_small      = pygame.font.SysFont('arial', \
                                                   CONFIG.FONTSIZE_SMALL)
        self.font_small_bold = pygame.font.SysFont('arial', \
                                                   CONFIG.FONTSIZE_SMALL, True)
        self.font_tiny       = pygame.font.SysFont('arial', \
                                                   CONFIG.FONTSIZE_TINY)


    def drawSeperatorLine (self, ypos):
        """draws a seperator line"""
        pygame.draw.line(self.screen, CONFIG.COLORS.SEP, \
                         (CONFIG.MARGIN, ypos),          \
                         (CONFIG.WIDTH-CONFIG.MARGIN, ypos), 2)
        return ypos + 5


    def drawItem (self, valuestring, font, color, ypos):
        """prints one line of text and increases ypos accordingly"""
        (_, _h) = font.size(valuestring)
        text = font.render(valuestring, True, color, CONFIG.COLORS.BACKGROUND)
        self.screen.blit(text, (CONFIG.MARGIN, ypos))
        ypos += _h
        return ypos


    def drawWeatherItem (self, room, value1, value2, value3, color, ypos):
        """prints all weather data of one screen section"""
        ypos = self.drawSeperatorLine(ypos)
        ypos = self.drawItem(room, self.font_tiny, CONFIG.COLORS.DESC, ypos)
        if value1 is not None:
            ypos = self.drawItem(value1, self.font, color, ypos)
        if value2 is not None:
            ypos = self.drawItem(value2, self.font, color, ypos)
        if value3 is not None:
            ypos = self.drawItem(value3, self.font, color, ypos)
        return ypos


    def drawSwitchValue (self, switch1, switch2, color, ypos):
        """prints values of switches"""
        ypos = self.drawItem(switch1, self.font_small, color, ypos)
        ypos = self.drawItem(switch2, self.font_small, color, ypos)
        return ypos


    def drawTime (self):
        """prints date and time at bottom of display"""
        self.drawSeperatorLine(CONFIG.HEIGHT- \
                               2*CONFIG.FONTSIZE_SMALL-int(2.5*CONFIG.SEP_Y))

        timestamp = localtime()
        A = CONSTANTS.DAYOFWEEK[strftime("%w", timestamp)]
        d = re.sub('^0', '', strftime("%d", timestamp))
        m = re.sub('^0', '', strftime("%m", timestamp))
        y = strftime("%Y", timestamp)
        datestr = "%s, %s. %s. %s" % (A, d, m, y)
        (w, _) = self.font_small.size(datestr)
        text = self.font_small.render(datestr, True, \
                                      CONFIG.COLORS.DATE, \
                                      CONFIG.COLORS.BACKGROUND)
        self.screen.blit(text, ((CONFIG.WIDTH-w)/2, \
                         CONFIG.HEIGHT-2*CONFIG.FONTSIZE_SMALL-2*CONFIG.SEP_Y))

        datestr = strftime("%H:%M:%S", timestamp) 
        (w, _) = self.font_small_bold.size(datestr)
        text = self.font_small_bold.render(datestr, True, \
                                           CONFIG.COLORS.DATE, \
                                           CONFIG.COLORS.BACKGROUND)
        self.screen.blit(text, ((CONFIG.WIDTH-w)/2, \
                         CONFIG.HEIGHT-CONFIG.FONTSIZE_SMALL-CONFIG.SEP_Y))


    def drawPicture (self, pathToPic, scale, ypos):
        """loads, scales, and prints ad picture"""
        surface_picture = pygame.image.load(pathToPic)
        (pw, ph) = surface_picture.get_size()
        pw = int(pw*scale)
        ph = int(ph*scale)
        surface_picture = pygame.transform.smoothscale(surface_picture, (pw, ph))
        (pw, ph) = surface_picture.get_size()
        self.screen.blit(surface_picture, (int((CONFIG.WIDTH-pw)/2), ypos))


###############################################################################
###############################################################################
class Screens (object):
    """manage various screens changed by a touching the touchscreen"""
    def __init__(self, display):
        self.display    = display
        self.__screenid = 1
        self.__screens  = {1: self.Screen1, \
                          2: self.Screen2, \
                          3: self.Screen3}


    @property
    def screenid (self):
        """getter for screenid"""
        return self.__screenid


    @screenid.setter
    def screenid (self, sid):
        """add +1 to screenid whenever the touchscreen has been touched"""
        if (sid <= 1):
            self.__screenid = 1
        elif (sid > len(self.__screens)):
            self.__screenid = 1
        else:
            self.__screenid = sid


    def Screen (self):
        """calls Screen<n>() whereat n == screenid"""
        self.__screens[self.screenid]()


    def Screen1 (self):
        """living room and outdoor"""
        ypos = CONFIG.MARGIN 
        self.display.screen.fill(CONFIG.COLORS.BACKGROUND)

        v1 = "-33,3 °C"
        v2 = "67,2 % rF"
        ypos = self.display.drawWeatherItem("Wohnzimmer:", \
                                            v1, v2, None,  \
                                            CONFIG.COLORS.INDOOR, ypos)
        ypos += CONFIG.SEP_Y

        v1 = "17,9 °C"
        v2 = "45,2 % rF"
        v3 = "1021 hPa"
        ypos  = self.display.drawWeatherItem("Draußen:", \
                                             v1, v2, v3, \
                                             CONFIG.COLORS.OUTDOOR, ypos)
        ypos += CONFIG.SEP_Y
        self.display.drawTime()


    def Screen2 (self):
        """kid's room"""
        ypos = CONFIG.MARGIN 
        self.display.screen.fill(CONFIG.COLORS.BACKGROUND)

        v1 = "-22,2 °C"
        v2 = "99,9 % rF"
        ypos = self.display.drawWeatherItem("Kinderzimmer:", \
                                            v1, v2, None,    \
                                            CONFIG.COLORS.KIDSROOM, ypos)
        ypos += CONFIG.SEP_Y
        self.display.drawPicture(os.path.join('data', 'child.png'), 0.8, ypos)
        self.display.drawTime()


    def Screen3 (self):
        """turtle's compound"""
        ypos = CONFIG.MARGIN 
        self.display.screen.fill(CONFIG.COLORS.BACKGROUND)

        v1 = "-13,3 °C"
        v2 = "100,0 % rF"
        v3 = "Heizung: ein"
        v4 = "Beleuchtung: aus"
        ypos = self.display.drawWeatherItem("Gehege Donut:", \
                                            v1, v2, None,    \
                                            CONFIG.COLORS.TURTLE, ypos)
        ypos = self.display.drawSwitchValue(v3, v4, CONFIG.COLORS.TURTLE, ypos)
        ypos += CONFIG.SEP_Y
        self.display.drawPicture(os.path.join('data', 'turtle.png'), 0.4, ypos)
        self.display.drawTime()


###############################################################################
# Main ########################################################################
def Main():
    pygame.init()
    pygame.mouse.set_visible(False)

    display = Display()
    screens = Screens(display)

    i = timestamp = 0
    while True:
        if (i >= 10):
            if (time() >= timestamp): # fallback to screenid #1 
                screens.screenid = 1

            screens.Screen()
            pygame.display.update()
            i = 0

        for event in pygame.event.get():
            if event.type == QUIT:
                Exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                screens.screenid += 1
                timestamp = time() + CONFIG.TIMETOFALLBACK

        pygame.time.delay(50)
        i += 1


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

