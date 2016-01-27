# -*- coding: utf-8 -*-
###############################################################################
# Screens.py                                                                  #
# (c) https://github.com/thomaspfeiffer-git 2016                              #
###############################################################################
"""
Different screens for Weatherstation.py
Currently there are three screens:
1) Living room and outside
2) Kid's room
3) Turtle's compound 
"""


import pygame
from Config import CONFIG
from Display import Display


def __getvalue (sensorvalue):
    """returns measured value of sensor or "n/a" if sensorvalue == None"""
    if sensorvalue is not None:
        return sensorvalue.value.encode('latin-1')
    else:
        return "(n/a)".encode('latin-1')


###############################################################################
class Screens (object):
    """manage various screens changed by a touching the touchscreen"""
    def __init__(self, display):
        self.display    = display
        self.__screenid = 1
        self.__screens  = {1: self.Screen1, \
                           2: self.Screen2, \
                           3: self.Screen3}

    @property
    def screenid (self):
        """getter for screenid"""
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

    def drawScreen (self, allsensorvalues):
        """calls Screen<n>() whereat n == screenid"""
        self.__screens[self.screenid](allsensorvalues)
        pygame.display.update()


    def Screen1 (self, allsensorvalues):
        """living room and outdoor"""
        ypos = CONFIG.MARGIN 
        self.display.screen.fill(CONFIG.COLORS.BACKGROUND)

        ypos = self.display.drawWeatherItem("Wohnzimmer:", \
                                            __getvalue(allsensorvalues['ID_01']), \
                                            __getvalue(allsensorvalues['ID_02']), \
                                            None,  \
                                            CONFIG.COLORS.INDOOR, ypos)
        ypos += CONFIG.SEP_Y

        if allsensorvalues['ID_05'] is not None:
            pressure = float(allsensorvalues['ID_05'].valuenumber.replace(',', '.'))
        else:
            pressure = 1013.25

        if pressure > 1000.0:
            picture = CONFIG.IMAGES.ICON_SUNNY
        elif pressure > 990.0:
            picture = CONFIG.IMAGES.ICON_CLOUDY
        elif pressure > 980.0:
            picture = CONFIG.IMAGES.ICON_OVERCAST
        else:
            picture = CONFIG.IMAGES.ICON_RAINY

        self.display.drawPicture(picture, 0.3, 
                                 xpos=Display.Position.Right, 
                                 ypos=ypos+CONFIG.MARGIN)
        ypos = self.display.drawWeatherItem(u'Draußen:', \
                                            __getvalue(allsensorvalues['ID_12']), \
                                            __getvalue(allsensorvalues['ID_04']), \
                                            __getvalue(allsensorvalues['ID_05']), \
                                            CONFIG.COLORS.OUTDOOR, ypos)
        ypos += CONFIG.SEP_Y
        self.display.drawTime()


    def Screen2 (self, allsensorvalues):
        """kid's room"""
        ypos = CONFIG.MARGIN 
        self.display.screen.fill(CONFIG.COLORS.BACKGROUND)

        ypos = self.display.drawWeatherItem("Kinderzimmer:", \
                                            __getvalue(allsensorvalues['ID_06']), \
                                            __getvalue(allsensorvalues['ID_07']), \
                                            None,    \
                                            CONFIG.COLORS.KIDSROOM, ypos)
        ypos += CONFIG.SEP_Y
        self.display.drawPicture(CONFIG.IMAGES.PIC_KIDSROOM, 0.8, 
                                 xpos=Display.Position.Center, ypos=ypos)
        self.display.drawTime()


    def Screen3 (self, allsensorvalues):
        """turtle's compound"""
        ypos = CONFIG.MARGIN 
        self.display.screen.fill(CONFIG.COLORS.BACKGROUND)

        ypos = self.display.drawWeatherItem("Gehege Donut:", \
                                            __getvalue(allsensorvalues['ID_08']), \
                                            __getvalue(allsensorvalues['ID_09']), \
                                            None,    \
                                            CONFIG.COLORS.TURTLE, ypos)
        ypos = self.display.drawSwitchValue(__getvalue(allsensorvalues['ID_10']), \
                                            __getvalue(allsensorvalues['ID_11']), \
                                            CONFIG.COLORS.TURTLE, ypos)
        ypos += CONFIG.SEP_Y
        self.display.drawPicture(CONFIG.IMAGES.PIC_TURTLE, 0.4, 
                                 xpos=Display.Position.Center, ypos=ypos)
        self.display.drawTime()

# eof #

