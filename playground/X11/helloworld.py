#!/usr/bin/python3


import os
import pygame
from pygame.locals import *
from random import randrange
import signal
import sys
from time import sleep
import traceback


os.environ["SDL_FBDEV"] = "/dev/fb1"
# os.environ["SDL_MOUSEDEV"] = "/dev/input/touchscreen"
# os.environ["SDL_MOUSEDRV"] = "TSLIB"
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Screen
width  = 480
height = 320
size = (width, height)
screen = pygame.display.set_mode(size, pygame.NOFRAME)



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
    pygame.display.set_caption("Hallo!")
    screen.fill((255,255,255))

    while True:
        pygame.draw.circle(screen, randcolor(), randcoor(), randdiameter())
        pygame.display.update()

        for event in pygame.event.get():
           if event.type == QUIT:
              Exit()

        sleep(5)


###############################################################################
###############################################################################
if __name__ == '__main__':
    signal.signal(signal.SIGTERM, _Exit)

    try:
        Main()

    except KeyboardInterrupt:
        Exit()

    except SystemExit:                  # Done in signal handler (method _Exit()) #
        pass

    except:
        print(traceback.print_exc())

    finally:        # All cleanup is done in KeyboardInterrupt or signal handler. #
        pass

# eof #



