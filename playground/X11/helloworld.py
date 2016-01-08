#!/usr/bin/python3


import os
import pygame
from pygame.locals import *
from random import randrange
import re
import signal
import string
import sys
from time import strftime, localtime
import traceback


os.environ["SDL_FBDEV"] = "/dev/fb1"
# os.environ["SDL_MOUSEDEV"] = "/dev/input/touchscreen"
# os.environ["SDL_MOUSEDRV"] = "TSLIB"
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Screen
width    = 320
height   = 480
fontsize       = int(height / 8)
sep            = int(fontsize / 5)
fontsize_small = int(fontsize / 2.4)

screen = pygame.display.set_mode((width, height), pygame.NOFRAME)

class CONFIG:
    COLOR_BG   = (255, 255, 255)
    COLOR_DATE = (0, 0, 0)
    COLOR_SEP  = (0, 0, 0)
   


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
def randcolor():
    color = (randrange(256), randrange(256), randrange(256))
    return color

###############################################################################
def randcoor():
    coor = (randrange(width), randrange(height))
    return coor

###############################################################################
def randdiameter():
    dia = randrange(width/5)
    return dia


###############################################################################
# Main ########################################################################
def Main():
    pygame.init()
    pygame.mouse.set_visible(False)
    screen.fill((255, 255, 255))

    font = pygame.font.SysFont('arial', fontsize)
    font_small = pygame.font.SysFont('arial', fontsize_small)

    text = font.render("-22,9 °C", True, (0, 0, 255), CONFIG.COLOR_BG)
    screen.blit(text, (0, 0))
    text = font.render("64,5 % rF", True, (0, 0, 255), CONFIG.COLOR_BG)
    screen.blit(text, (0, fontsize))

    text = font.render("23,4 °C", True, (255, 0, 0), CONFIG.COLOR_BG)
    screen.blit(text, (0, 2*fontsize+sep))
    text = font.render("64,5 % rF", True, (255, 0, 0), CONFIG.COLOR_BG)
    screen.blit(text, (0, 3*fontsize+sep))

    pygame.draw.line(screen, CONFIG.COLOR_SEP, (3, height-fontsize_small-int(1.5*sep)), \
                                               (width-3, height-fontsize_small-int(1.5*sep)), 2)

    i = 0
    while True:
        if (i >= 100):
            timestamp = localtime()
            A = strftime("%a", timestamp)
            d = re.sub('^0', '', strftime("%d", timestamp))
            m = re.sub('^0', '', strftime("%m", timestamp))
            y = strftime("%Y", timestamp)
            datestr = "%s, %s. %s. %s" % (A, d, m, y)
            text = font_small.render(datestr, True, CONFIG.COLOR_DATE, CONFIG.COLOR_BG)
            screen.blit(text, (sep, height-fontsize_small-sep))

            datestr = strftime("%H:%M:%S", timestamp) 
            text = font_small.render(datestr, True, CONFIG.COLOR_DATE, CONFIG.COLOR_BG)
            (w, h) = font_small.size(datestr)
            screen.blit(text, (width-w-sep, height-fontsize_small-sep))

            pygame.display.update()
            i = 0

        for event in pygame.event.get():
            if event.type == QUIT:
                Exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                print("Mausklick")

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

