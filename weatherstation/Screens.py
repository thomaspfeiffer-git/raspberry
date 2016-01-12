# -*- coding: utf-8 -*-

import os

from Config import CONFIG


###############################################################################
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


    def Screen (self, allsensorvalues):
        """calls Screen<n>() whereat n == screenid"""
        self.__screens[self.screenid](allsensorvalues)


    def Screen1 (self, allsensorvalues):
        """living room and outdoor"""
        ypos = CONFIG.MARGIN 
        self.display.screen.fill(CONFIG.COLORS.BACKGROUND)

        ypos = self.display.drawWeatherItem("Wohnzimmer:", \
                                            allsensorvalues.read('ID_01'), \
                                            allsensorvalues.read('ID_02'), \
                                            None,  \
                                            CONFIG.COLORS.INDOOR, ypos)
        ypos += CONFIG.SEP_Y

        ypos = self.display.drawWeatherItem(u'Draußen:', \
                                            allsensorvalues.read('ID_03'), \
                                            allsensorvalues.read('ID_04'), \
                                            allsensorvalues.read('ID_05'), \
                                            CONFIG.COLORS.OUTDOOR, ypos)
        ypos += CONFIG.SEP_Y
        self.display.drawTime()


    def Screen2 (self, allsensorvalues):
        """kid's room"""
        ypos = CONFIG.MARGIN 
        self.display.screen.fill(CONFIG.COLORS.BACKGROUND)

        ypos = self.display.drawWeatherItem("Kinderzimmer:", \
                                            allsensorvalues.read('ID_06'), \
                                            allsensorvalues.read('ID_07'), \
                                            None,    \
                                            CONFIG.COLORS.KIDSROOM, ypos)
        ypos += CONFIG.SEP_Y
        self.display.drawPicture(os.path.join('data', 'child.png'), 0.8, ypos)
        self.display.drawTime()


    def Screen3 (self, allsensorvalues):
        """turtle's compound"""
        ypos = CONFIG.MARGIN 
        self.display.screen.fill(CONFIG.COLORS.BACKGROUND)

        ypos = self.display.drawWeatherItem("Gehege Donut:", \
                                            allsensorvalues.read('ID_08'), \
                                            allsensorvalues.read('ID_09'), \
                                            None,    \
                                            CONFIG.COLORS.TURTLE, ypos)
        ypos = self.display.drawSwitchValue(allsensorvalues.read('ID_10'), \
                                            allsensorvalues.read('ID_11'), \
                                            CONFIG.COLORS.TURTLE, ypos)
        ypos += CONFIG.SEP_Y
        self.display.drawPicture(os.path.join('data', 'turtle.png'), 0.4, ypos)
        self.display.drawTime()

# eof #

