# -*- coding: utf-8 -*-
###############################################################################
# Display.py                                                                  #
# (c) https://github.com/thomaspfeiffer-git 2016                              #
###############################################################################
"""all about displaying the various weather values on several screens"""


import os
import pygame
import re
from time import strftime, localtime

from Config import CONFIG
from Constants import CONSTANTS


###############################################################################
###############################################################################
class Display (object):
    """all about displaying the various weather values on several screens"""

    class Position:
        """enum for positioning"""
        Left, Center, Right, Top, Bottom = range(5)

    def __init__ (self):
        os.environ["SDL_FBDEV"] = "/dev/fb1" 
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        pygame.mixer.quit() # no audio needed; shall be useable by other applications
        pygame.mouse.set_visible(False)

        self.screen = pygame.display.set_mode((CONFIG.WIDTH, CONFIG.HEIGHT), \
                                               pygame.NOFRAME)
        self.screen.fill(CONFIG.COLORS.BACKGROUND)

        self.font            = pygame.font.SysFont('arial', \
                                                   CONFIG.FONTSIZE)
        self.font_small      = pygame.font.SysFont('arial', \
                                                   CONFIG.FONTSIZE_SMALL)
        self.font_forecast   = pygame.font.SysFont('arial', \
                                                   CONFIG.FONTSIZE_FORECAST)
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


    def drawForecastItem (self, room, value1, value2, value3, value4, color, ypos):
        """prints all weather data of one screen section"""
        ypos = self.drawSeperatorLine(ypos)
        ypos = self.drawItem(room, self.font_tiny, CONFIG.COLORS.DESC, ypos)
        if value1 is not None:
            ypos = self.drawItem(value1, self.font_forecast, color, ypos)
        if value2 is not None:
            ypos = self.drawItem(value2, self.font_forecast, color, ypos)
        if value3 is not None:
            ypos = self.drawItem(value3, self.font_forecast, color, ypos)
        if value4 is not None:
            ypos = self.drawItem(value4, self.font_forecast, color, ypos)
        return ypos


    def drawWeatherItem (self, room, value1, value2, value3, value4, color, ypos):
        """prints all weather data of one screen section"""
        ypos = self.drawSeperatorLine(ypos)
        ypos = self.drawItem(room, self.font_tiny, CONFIG.COLORS.DESC, ypos)
        if value1 is not None:
            ypos = self.drawItem(value1, self.font, color, ypos)
        if value2 is not None:
            ypos = self.drawItem(value2, self.font, color, ypos)
        if value3 is not None:
            ypos = self.drawItem(value3, self.font, color, ypos)
        if value4 is not None:
            ypos = self.drawItem(value4, self.font, color, ypos)
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
        self.screen.blit(text, ((CONFIG.WIDTH-w-CONFIG.MARGIN), \
                         CONFIG.HEIGHT-2*CONFIG.FONTSIZE_SMALL-2*CONFIG.SEP_Y))

        datestr = strftime("%H:%M:%S", timestamp) 
        (w, _) = self.font_small_bold.size(datestr)
        text = self.font_small_bold.render(datestr, True, \
                                           CONFIG.COLORS.DATE, \
                                           CONFIG.COLORS.BACKGROUND)
        self.screen.blit(text, ((CONFIG.WIDTH-w-CONFIG.MARGIN), \
                         CONFIG.HEIGHT-CONFIG.FONTSIZE_SMALL-CONFIG.SEP_Y))


    def drawPicture (self, pathToPic, scale, xpos, ypos):
        """loads, scales, and prints a picture"""
        surface_picture = pygame.image.load(pathToPic)
        (pw, ph) = surface_picture.get_size()
        pw = int(pw*scale)
        ph = int(ph*scale)
        surface_picture = pygame.transform.smoothscale(surface_picture, (pw, ph))
        (pw, ph) = surface_picture.get_size()
        if xpos == Display.Position.Center:
            x = int((CONFIG.WIDTH-pw)/2)
        elif xpos == Display.Position.Right:
            x = CONFIG.WIDTH-CONFIG.MARGIN-pw
        elif xpos == Display.Position.Left:
            x = CONFIG.MARGIN
        else:
            raise ValueError("unknown value for xpos in Display.drawPicture()")
        self.screen.blit(surface_picture, (x, ypos))

# eof #

