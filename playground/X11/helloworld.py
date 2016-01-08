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

screen = pygame.display.set_mode((width, height), pygame.NOFRAME)

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


###############################################################################
# Main ########################################################################
def Main():
    pygame.init()
    pygame.mouse.set_visible(False)
    screen.fill((255, 255, 255))

    font = pygame.font.SysFont('arial', fontsize)
    font_small = pygame.font.SysFont('arial', fontsize_small)
    font_small_bold = pygame.font.SysFont('arial', fontsize_small, True)
    font_tiny       = pygame.font.SysFont('arial', fontsize_tiny)

    h = 0
    # Seperator Indoor #
    pygame.draw.line(screen, CONFIG.COLOR_SEP, (3, 3), (width-3, 3), 2)
    h += 8
    valuestring = "Wohnzimmer:"
    (_, _h) = font_tiny.size(valuestring)
    text = font_tiny.render(valuestring, True, CONFIG.COLOR_DESC, CONFIG.COLOR_BG)
    screen.blit(text, (3, 6))
    h += _h

    valuestring = "-22,2 °C"
    (_, _h) = font.size(valuestring)
    text = font.render(valuestring, True, CONFIG.COLOR_INDOOR, CONFIG.COLOR_BG)
    screen.blit(text, (3, h))
    h += _h + 5

    valuestring = "47,9 % rF"
    (_, _h) = font.size(valuestring)
    text = font.render(valuestring, True, CONFIG.COLOR_INDOOR, CONFIG.COLOR_BG)
    screen.blit(text, (3, h))
    h += _h + 5


    # Seperator Outdoor #
    h += sep
    pygame.draw.line(screen, CONFIG.COLOR_SEP, (3, h), (width-3, h), 2)
    h += 8
    valuestring = "Draußen:"
    (_, _h) = font_tiny.size(valuestring)
    text = font_tiny.render(valuestring, True, CONFIG.COLOR_DESC, CONFIG.COLOR_BG)
    screen.blit(text, (3, h))
    h += _h
    
    valuestring = "-22,2 °C"
    (_, _h) = font.size(valuestring)
    text = font.render(valuestring, True, CONFIG.COLOR_OUTDOOR, CONFIG.COLOR_BG)
    screen.blit(text, (3, h))
    h += _h + 5

    valuestring = "47,9 % rF"
    (_, _h) = font.size(valuestring)
    text = font.render(valuestring, True, CONFIG.COLOR_OUTDOOR, CONFIG.COLOR_BG)
    screen.blit(text, (3, h))
    h += _h + 5





    # Seperator Date #
    pygame.draw.line(screen, CONFIG.COLOR_SEP, \
                             (3, height-2*fontsize_small-int(2.5*sep)), \
                             (width-3, height-2*fontsize_small-int(2.5*sep)), 2)

#    text = font.render("-22,9 °C", True, (0, 0, 255), CONFIG.COLOR_BG)
#    screen.blit(text, (0, 0))
#    text = font.render("64,5 % rF", True, (0, 0, 255), CONFIG.COLOR_BG)
#    screen.blit(text, (0, fontsize))

#    text = font.render("23,4 °C", True, (255, 0, 0), CONFIG.COLOR_BG)
#    screen.blit(text, (0, 2*fontsize+sep))
#    text = font.render("64,5 % rF", True, (255, 0, 0), CONFIG.COLOR_BG)
#    screen.blit(text, (0, 3*fontsize+sep))


    i = 0
    while True:
        if (i >= 100):
            timestamp = localtime()
            A = DayOfWeek[strftime("%w", timestamp)]
            d = re.sub('^0', '', strftime("%d", timestamp))
            m = re.sub('^0', '', strftime("%m", timestamp))
            y = strftime("%Y", timestamp)
            datestr = "%s, %s. %s. %s" % (A, d, m, y)
            (w, h) = font_small.size(datestr)
            text = font_small.render(datestr, True, CONFIG.COLOR_DATE, CONFIG.COLOR_BG)
            screen.blit(text, ((width-w)/2, height-2*fontsize_small-2*sep))

            datestr = strftime("%H:%M:%S", timestamp) 
            (w, h) = font_small_bold.size(datestr)
            text = font_small_bold.render(datestr, True, CONFIG.COLOR_DATE, CONFIG.COLOR_BG)
            screen.blit(text, ((width-w)/2, height-fontsize_small-sep))

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

