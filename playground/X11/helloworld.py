#!/usr/bin/python3


import os
import pygame
from pygame.locals import *
import re
import signal
import string
import sys
from time import strftime, localtime, sleep
import traceback


os.environ["SDL_FBDEV"] = "/dev/fb1"
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Screen
width    = 320
height   = 480
fontsize       = int(height / 8)
sep            = int(fontsize / 5)
fontsize_small = int(fontsize / 2.4)
fontsize_tiny  = int(fontsize / 3.4)


class CONFIG:
    COLOR_BG   = (255, 255, 255)
    COLOR_DATE = (0, 0, 0)
    COLOR_DESC = (0, 0, 0)
    COLOR_SEP  = (0, 0, 0)
    COLOR_INDOOR   = (255, 0, 0)
    COLOR_OUTDOOR  = (0, 0, 255)
    COLOR_KIDSROOM = (0, 255, 0)


DayOfWeek = {'0': 'Sonntag',    \
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
    def __init__(self):
        self.screen = pygame.display.set_mode((width, height), pygame.NOFRAME)
        self.screen.fill(CONFIG.COLOR_BG)

        self.font = pygame.font.SysFont('arial', fontsize)
        self.font_small = pygame.font.SysFont('arial', fontsize_small)
        self.font_small_bold = pygame.font.SysFont('arial', fontsize_small, True)
        self.font_tiny       = pygame.font.SysFont('arial', fontsize_tiny)

    def drawSeperatorLine (self, ypos):
        pygame.draw.line(self.screen, CONFIG.COLOR_SEP, (3, ypos), (width-3, ypos), 2)
        return ypos + 5

    def drawItem (self, valuestring, font, color, ypos):
        (_, _h) = font.size(valuestring)
        text = font.render(valuestring, True, color, CONFIG.COLOR_BG)
        self.screen.blit(text, (3, ypos))
        ypos += _h
        return ypos

    def drawWeatherItem (self, room, value1, value2, value3, color, ypos):
        ypos = self.drawSeperatorLine(ypos)
        ypos = self.drawItem(room, self.font_tiny, CONFIG.COLOR_DESC, ypos)
        if value1 is not None:
            ypos = self.drawItem(value1, self.font, color, ypos)
        if value2 is not None:
            ypos = self.drawItem(value2, self.font, color, ypos)
        if value3 is not None:
            ypos = self.drawItem(value3, self.font, color, ypos)
        return ypos


    def drawTime (self):
        self.drawSeperatorLine(height-2*fontsize_small-int(2.5*sep))

        timestamp = localtime()
        A = DayOfWeek[strftime("%w", timestamp)]
        d = re.sub('^0', '', strftime("%d", timestamp))
        m = re.sub('^0', '', strftime("%m", timestamp))
        y = strftime("%Y", timestamp)
        datestr = "%s, %s. %s. %s" % (A, d, m, y)
        (w, h) = self.font_small.size(datestr)
        text = self.font_small.render(datestr, True, CONFIG.COLOR_DATE, CONFIG.COLOR_BG)
        self.screen.blit(text, ((width-w)/2, height-2*fontsize_small-2*sep))

        datestr = strftime("%H:%M:%S", timestamp) 
        (w, h) = self.font_small_bold.size(datestr)
        text = self.font_small_bold.render(datestr, True, CONFIG.COLOR_DATE, CONFIG.COLOR_BG)
        self.screen.blit(text, ((width-w)/2, height-fontsize_small-sep))


###############################################################################
###############################################################################
class Screen (object):
    """manage various screens changed by a touching the touchscreen"""
    def __init__(self, display):
        self.display   = display
        self.screenid  = 1
        self.__screens = {1: self.Screen1, \
                          2: self.Screen2, \
                          3: self.Screen3}

    @property
    def screenid (self):
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
        self.__screens[self.screenid]()

    def Screen1 (self):
        h = 3
        self.display.screen.fill(CONFIG.COLOR_BG)

        v1 = "-33,3 °C"
        v2 = "67,2 % rF"
        h = self.display.drawWeatherItem("Wohnzimmer:", v1, v2, None, CONFIG.COLOR_INDOOR, h)
        h += sep

        v1 = "17,9 °C"
        v2 = "45,2 % rF"
        v3 = "1021 hPa"
        h  = self.display.drawWeatherItem("Draußen:", v1, v2, v3, CONFIG.COLOR_OUTDOOR, h)
        h += sep

        self.display.drawTime()

    def Screen2 (self):
        h = 3
        self.display.screen.fill(CONFIG.COLOR_BG)

        v1 = "-22,2 °C"
        v2 = "99,9 % rF"
        h = self.display.drawWeatherItem("Kinderzimmer:", v1, v2, None, CONFIG.COLOR_KIDSROOM, h)
        h += sep

        surface_picture = pygame.image.load(os.path.join('data', 'child.png')).convert()
        (pw, ph) = surface_picture.get_size()
        pw = int(pw*0.8)
        ph = int(ph*0.8)
        surface_picture = pygame.transform.scale(surface_picture, (pw, ph))
        (pw, ph) = surface_picture.get_size()
        self.display.screen.blit(surface_picture, (int((width-pw)/2),h))

        self.display.drawTime()

    def Screen3 (self):
        self.display.screen.fill(CONFIG.COLOR_BG)
        self.display.drawTime()


###############################################################################
# Main ########################################################################
def Main():
    pygame.init()
    pygame.mouse.set_visible(False)

    display = Display()
    screens = Screen(display)

    i = 0
    while True:
        if (i >= 10):
            screens.Screen()
            pygame.display.update()
            i = 0

        for event in pygame.event.get():
            if event.type == QUIT:
                Exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                screens.screenid += 1

        # pygame.time.delay(100)
        sleep(10)
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

