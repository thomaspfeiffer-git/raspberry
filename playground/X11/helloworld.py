#!/usr/bin/python3

import pygame
from pygame.local import *
from time import sleep

(B, H) = (FULLSCREEN, FULLSCREEN)

pygame.init()
surf = pygame.display.set_mode((B, H), 0, 32)

pygame.display.set_caption("Hallo!")

surf.fill((255,255,255))
pygame.display.update()



while True:
    sleep(0.1)
