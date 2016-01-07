#!/usr/bin/python3


import os
import sys
import pygame
from pygame.locals import *

os.environ["SDL_FBDEV"] = "/dev/fb0"
os.environ["SDL_MOUSEDEV"] = "/dev/input/touchscreen"
os.environ["SDL_MOUSEDRV"] = "TSLIB"
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Screen
width  = 480
height = 320
size = (width, height)
screen = pygame.display.set_mode(size, pygame.NOFRAME)
pygame.init()


pygame.display.set_caption("Hallo!")
screen.fill((255,255,255))

pygame.draw.circle(screen, (255, 0, 0), (100, 100), 100)

pygame.display.update()



while True:
    sleep(0.1)
