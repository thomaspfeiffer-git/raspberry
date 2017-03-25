# -*- coding: utf-8 -*-
###############################################################################
# Button.py                                                                   #
# (c) https://github.com/thomaspfeiffer-git 2016                              #
###############################################################################
"""   """



# https://github.com/Mekire/pygame-button/blob/master/button/button.py
# https://github.com/asweigart/pygbutton/blob/master/pygbutton/__init__.py


import pygame
from pygame.locals import *


BLACK     = (  0,   0,   0)
WHITE     = (255, 255, 255)
DARKGRAY  = ( 64,  64,  64)
GRAY      = (128, 128, 128)
LIGHTGRAY = (212, 208, 200)


class Button (object):
    def __init__ (self, screen=None, rect=None, caption='', bgcolor=LIGHTGRAY, fgcolor=BLACK, font=None):
   
        if screen is None:
            pass
            # TODO: raise exception
        else:
            self._screen = screen
 
        if rect is None:
            pass
            # TODO: raise exception
        else:
            self._rect = pygame.Rect(rect)

        self._caption = caption
        self._bgcolor = bgcolor
        self._fgcolor = fgcolor

        if font is None:
            pass
            # TODO: raise exception
        else:
            self._font = font

        self._surface = pygame.Surface(self._rect.size)

        self._update()


    def draw (self):
        self._screen.blit(self._surface, self._rect)


    def _update (self):
        w = self._rect.width
        h = self._rect.height 

        self._surface.fill(self._bgcolor)

        caption = self._font.render(self._caption, True, self._fgcolor, self._bgcolor)
        captionRect = caption.get_rect()
        captionRect.center = int(w / 2), int(h / 2)
        self._surface.blit(caption, captionRect)

        pygame.draw.rect(self._surface, BLACK, pygame.Rect((0, 0, w, h)), 1)
        pygame.draw.line(self._surface, WHITE, (1, 1), (w - 2, 1))
        pygame.draw.line(self._surface, WHITE, (1, 1), (1, h - 2))
        pygame.draw.line(self._surface, DARKGRAY, (1, h - 1), (w - 1, h - 1))
        pygame.draw.line(self._surface, DARKGRAY, (w - 1, 1), (w - 1, h - 1))
        pygame.draw.line(self._surface, GRAY, (2, h - 2), (w - 2, h - 2))
        pygame.draw.line(self._surface, GRAY, (w - 2, 2), (w - 2, h - 2))




# eof #

