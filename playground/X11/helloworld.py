#!/usr/bin/python3


import os
import signal
import sys
import pygame
from pygame.locals import *
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
# Main ########################################################################
def Main():
    pygame.init()
    pygame.display.set_caption("Hallo!")
    screen.fill((255,255,255))

    pygame.draw.circle(screen, (255, 0, 0), (100, 100), 100)
    pygame.draw.circle(screen, (0, 255, 0), (200, 200), 100)
    pygame.draw.circle(screen, (0, 0, 255), (300, 300), 100)

    pygame.display.update()

    while True:
        event = pygame.event.wait()
        if ((event.type == KEYDOWN) or (event.type == QUIT)):
            Exit()
        sleep(0.1)



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



