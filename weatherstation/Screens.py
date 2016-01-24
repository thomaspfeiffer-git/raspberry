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


import os
import pygame
from Config import CONFIG


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


    def __getvalue (self, sensorvalue):
        """returns measured value of sensor or "n/a" if sensorvalue == None"""
        if sensorvalue is not None:
            return sensorvalue.value.encode('latin-1')
        else:
            return "(n/a)".encode('latin-1')


    def Screen1 (self, allsensorvalues):
        """living room and outdoor"""
        ypos = CONFIG.MARGIN 
        self.display.screen.fill(CONFIG.COLORS.BACKGROUND)

        ypos = self.display.drawWeatherItem("Wohnzimmer:", \
                                            self.__getvalue(allsensorvalues['ID_01']), \
                                            self.__getvalue(allsensorvalues['ID_02']), \
                                            None,  \
                                            CONFIG.COLORS.INDOOR, ypos)
        ypos += CONFIG.SEP_Y

        pressure = self.__getvalue(allsensorvalues['ID_05'])
        print "Druck:", pressure

        self.display.drawPicture(os.path.join('data', 'symbol_sunny.png'), 0.4, xpos="r", ypos=ypos)
        ypos = self.display.drawWeatherItem(u'Draußen:', \
                                            self.__getvalue(allsensorvalues['ID_12']), \
                                            self.__getvalue(allsensorvalues['ID_04']), \
                                            self.__getvalue(allsensorvalues['ID_05']), \
                                            CONFIG.COLORS.OUTDOOR, ypos)
        ypos += CONFIG.SEP_Y
        self.display.drawTime()


    def Screen2 (self, allsensorvalues):
        """kid's room"""
        ypos = CONFIG.MARGIN 
        self.display.screen.fill(CONFIG.COLORS.BACKGROUND)

        ypos = self.display.drawWeatherItem("Kinderzimmer:", \
                                            self.__getvalue(allsensorvalues['ID_06']), \
                                            self.__getvalue(allsensorvalues['ID_07']), \
                                            None,    \
                                            CONFIG.COLORS.KIDSROOM, ypos)
        ypos += CONFIG.SEP_Y
        self.display.drawPicture(os.path.join('data', 'child.png'), 0.8, xpos="c", ypos=ypos)
        self.display.drawTime()


    def Screen3 (self, allsensorvalues):
        """turtle's compound"""
        ypos = CONFIG.MARGIN 
        self.display.screen.fill(CONFIG.COLORS.BACKGROUND)

        ypos = self.display.drawWeatherItem("Gehege Donut:", \
                                            self.__getvalue(allsensorvalues['ID_08']), \
                                            self.__getvalue(allsensorvalues['ID_09']), \
                                            None,    \
                                            CONFIG.COLORS.TURTLE, ypos)
        ypos = self.display.drawSwitchValue(self.__getvalue(allsensorvalues['ID_10']), \
                                            self.__getvalue(allsensorvalues['ID_11']), \
                                            CONFIG.COLORS.TURTLE, ypos)
        ypos += CONFIG.SEP_Y
        self.display.drawPicture(os.path.join('data', 'turtle.png'), 0.4, xpos="c", ypos=ypos)
        self.display.drawTime()

# eof #

