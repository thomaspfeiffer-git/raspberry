#!/usr/bin/python3


import os
import pygame
from pygame.locals import *
import re
import signal
import string
import sys
from time import strftime, localtime
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
    COLOR_INDOOR  = (255, 0, 0)
    COLOR_OUTDOOR = (0, 0, 255)


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


class Display (object):
    def __init__(self):
        self.screen = pygame.display.set_mode((width, height), pygame.NOFRAME)
        self.screen.fill((255, 255, 255))

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

    def drawWeatherItem (self, room, value1, value2, color, ypos):
        ypos = self.drawSeperatorLine(ypos)
        ypos = self.drawItem(room, self.font_tiny, CONFIG.COLOR_DESC, ypos)
        ypos = self.drawItem(value1, self.font, color, ypos)
        ypos = self.drawItem(value2, self.font, color, ypos)
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
# Main ########################################################################
def Main():
    pygame.init()
    pygame.mouse.set_visible(False)

    display = Display()

    i = 0
    while True:
        if (i >= 100):
            h = 3

            v1 = "-33,3 °C"
            v2 = "67,2 % rF"
            h = display.drawWeatherItem("Wohnzimmer:", v1, v2, CONFIG.COLOR_INDOOR, h)
            h += sep

            v1 = "17,9 °C"
            v2 = "45,2 % rF"
            h  = display.drawWeatherItem("Draußen:", v1, v2, CONFIG.COLOR_OUTDOOR, h)
            h += sep

            display.drawTime()

            pygame.display.update()
            i = 0

        for event in pygame.event.get():
            if event.type == QUIT:
                Exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pass

        pygame.time.wait(1)
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

