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
3) Cottage outside
4) Cottage inside
"""


import pygame
from Config import CONFIG
from Display import Display


def getvalue (sensorvalue):
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
        self.__screens  = {1: self.Screen1,
                           2: self.Screen_OWM,
                           3: self.Screen2,
                           4: self.Screen3,
                           5: self.Screen4,
                           6: self.Screen5,
                           7: self.Screen6}


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
                                            getvalue(allsensorvalues['ID_01']), \
                                            getvalue(allsensorvalues['ID_02']), \
                                            None,                               \
                                            None,                               \
                                            CONFIG.COLORS.INDOOR, ypos)
        ypos += CONFIG.SEP_Y

        if allsensorvalues['ID_05'] is not None:
            try:
                pressure = float(allsensorvalues['ID_05'].valuenumber.replace(',', '.'))

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
            except ValueError:
                pass

        ypos = self.display.drawWeatherItem("Draußen:", \
                                            getvalue(allsensorvalues['ID_12']), \
                                            getvalue(allsensorvalues['ID_04']), \
                                            getvalue(allsensorvalues['ID_05']), \
                                            None,                               \
                                            CONFIG.COLORS.OUTDOOR, ypos)
        ypos += CONFIG.SEP_Y
        self.display.drawTime()

    def Screen2 (self, allsensorvalues):
        """kid's room"""
        ypos = CONFIG.MARGIN 
        self.display.screen.fill(CONFIG.COLORS.BACKGROUND)

        ypos = self.display.drawWeatherItem("Kinderzimmer:", \
                                            getvalue(allsensorvalues['ID_06']), \
                                            getvalue(allsensorvalues['ID_07']), \
                                            None,                               \
                                            None,                               \
                                            CONFIG.COLORS.KIDSROOM, ypos)
        ypos += CONFIG.SEP_Y
        self.display.drawPicture(CONFIG.IMAGES.PIC_KIDSROOM, 0.8, 
                                 xpos=Display.Position.Center, ypos=ypos)
        self.display.drawTime()

    def Screen3 (self, allsensorvalues):
        """Kollerberg outside"""
        ypos = CONFIG.MARGIN 
        self.display.screen.fill(CONFIG.COLORS.BACKGROUND)

        ypos = self.display.drawWeatherItem("Kollerberg (außen):", \
                                            getvalue(allsensorvalues['ID_24']), \
                                            getvalue(allsensorvalues['ID_25']), \
                                            getvalue(allsensorvalues['ID_23']), \
                                            None,                               \
                                            CONFIG.COLORS.COTTAGE, ypos)
        ypos += CONFIG.SEP_Y
        self.display.drawPicture(CONFIG.IMAGES.PIC_COTTAGE, 0.8, 
                                 xpos=Display.Position.Center, ypos=ypos)
        self.display.drawTime()

    def Screen4 (self, allsensorvalues):
        """Kollerberg inside"""
        ypos = CONFIG.MARGIN 
        self.display.screen.fill(CONFIG.COLORS.BACKGROUND)

        ypos = self.display.drawWeatherItem("Kollerberg (innen):", \
                                            getvalue(allsensorvalues['ID_21']), \
                                            getvalue(allsensorvalues['ID_22']), \
                                            getvalue(allsensorvalues['ID_26']), \
                                            getvalue(allsensorvalues['ID_27']), \
                                            CONFIG.COLORS.COTTAGE, ypos)
        ypos += CONFIG.SEP_Y
        self.display.drawTime()

    def Screen6 (self, allsensorvalues):
        """misc sensor values"""
        ypos = CONFIG.MARGIN 
        self.display.screen.fill(CONFIG.COLORS.BACKGROUND)

        ypos = self.display.drawWeatherItem("Misc:", \
                                            getvalue(allsensorvalues['ID_03']), \
                                            getvalue(allsensorvalues['ID_13']), \
                                            None,    \
                                            None,    \
                                            CONFIG.COLORS.MISC, ypos)
        self.display.drawTime()

    def Screen5 (self, allsensorvalues):
        """Wardrobe"""
        ypos = CONFIG.MARGIN 
        self.display.screen.fill(CONFIG.COLORS.BACKGROUND)

        ypos = self.display.drawWeatherItem("Schlafzimmerkasten:", \
                                            getvalue(allsensorvalues['ID_31']), \
                                            getvalue(allsensorvalues['ID_32']), \
                                            getvalue(allsensorvalues['ID_33']), \
                                            None,    \
                                            CONFIG.COLORS.WARDROBE, ypos)
        self.display.drawTime()

    def Screen_OWM (self, allsensorvalues):
        """openweathermap"""
        ypos = CONFIG.MARGIN 
        self.display.screen.fill(CONFIG.COLORS.BACKGROUND)

        ypos = self.display.drawForecastItem("Wettervorhersage heute:", \
                                             getvalue(allsensorvalues['ID_OWM_05']), \
                                             getvalue(allsensorvalues['ID_OWM_01']) + b' - ' + \
                                                   getvalue(allsensorvalues['ID_OWM_02']), \
                                             getvalue(allsensorvalues['ID_OWM_03']) + b' (' + \
                                                   getvalue(allsensorvalues['ID_OWM_04']) + b')', \
                                             None, \
                                             CONFIG.COLORS.OUTDOOR, ypos)
        ypos = self.display.drawForecastItem("Wettervorhersage morgen:", \
                                             getvalue(allsensorvalues['ID_OWM_15']), \
                                             getvalue(allsensorvalues['ID_OWM_11']) + b' - ' + \
                                                   getvalue(allsensorvalues['ID_OWM_12']), \
                                             getvalue(allsensorvalues['ID_OWM_13']) + b' (' + \
                                                   getvalue(allsensorvalues['ID_OWM_14']) + b')', \
                                             None, \
                                             CONFIG.COLORS.OUTDOOR, ypos)
        ypos = self.display.drawForecastItem("Wettervorhersage übermorgen:", \
                                             getvalue(allsensorvalues['ID_OWM_25']), \
                                             getvalue(allsensorvalues['ID_OWM_21']) + b' - ' + \
                                                   getvalue(allsensorvalues['ID_OWM_22']), \
                                             getvalue(allsensorvalues['ID_OWM_23']) + b' (' + \
                                                   getvalue(allsensorvalues['ID_OWM_24']) + b')', \
                                             None, \
                                             CONFIG.COLORS.OUTDOOR, ypos)
        self.display.drawTime()

# eof #

