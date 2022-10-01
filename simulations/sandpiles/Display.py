# -*- coding: utf-8 -*-
###############################################################################
# Display.py                                                                  #
# (c) https://github.com/thomaspfeiffer-git/raspberry, 2019                   #
###############################################################################
"""
All display related stuff for Sandpiles.py.
"""

import os
from PIL import Image, ImageDraw
import tkinter as tk

from Config import CONFIG, filename
from Logging import Log

# When having these instances as members of DrawPile(), they seem
# to be garbagge collected for some reason. As a quick workaround,
# i make them global.
image = Image.new("RGB", (CONFIG.PILE.X, CONFIG.PILE.Y), (0, 0, 0))
draw = ImageDraw.Draw(image)

###############################################################################
# DrawPile ####################################################################
class DrawPile (tk.Frame):
    def __init__ (self, pile, master=None):
        super().__init__(master)

        self.pile = pile
        self.master = master

        self.canvas = tk.Canvas(self.master, bg=CONFIG.COLORS.BG_PILE,
                                width=CONFIG.PILE.X,
                                height=CONFIG.PILE.Y)
        self.canvas.pack()

        self.img = tk.PhotoImage(width=CONFIG.PILE.X, height=CONFIG.PILE.Y)
        self.canvas.create_image((CONFIG.PILE.X//2, CONFIG.PILE.Y//2), 
                                 image=self.img, state="normal")
        # self.image = Image.new("RGB", (CONFIG.PILE.X, CONFIG.PILE.Y), (0, 0, 0))
        # self.draw = ImageDraw.Draw(self.image)

    def draw (self):
        self.pile.localize()
        for x in range(CONFIG.PILE.X):
            for y in range(CONFIG.PILE.Y):
                try:
                    self.img.put(CONFIG.COLORS.GRAIN[self.pile.pile[x][y]], (x,y))
                    draw.point([x,y], CONFIG.COLORS.GRAIN[self.pile.pile[x][y]])
                except KeyError:
                    pass
        image.save(filename("png"))


###############################################################################
# TkApp #######################################################################
class TkApp (object):
    def __init__ (self, pile, do_draw):

        try:
            os.environ["DISPLAY"]
        except KeyError:
            Log("$DISPLAY not set, using default :0.0")
            os.environ["DISPLAY"] = ":0.0"
    
        self.pile = pile
        self.do_draw = do_draw

        self.root = tk.Tk()
        self.root.overrideredirect(1)
        self.root.config(cursor='none')
        self.root.resizable(width=False, height=False)

        self.root.width  = CONFIG.PILE.X
        self.root.height = CONFIG.PILE.Y+100 # TODO: make constant
        self.root.borderwidth = 0
        self.root.geometry("{}x{}+{}+{}".format(self.root.width,
                                                self.root.height,
                                                CONFIG.COORDINATES.XPOS,
                                                CONFIG.COORDINATES.YPOS))
        self.root.config(bg=CONFIG.COLORS.BG_TEXT)
        self.app = DrawPile(pile=self.pile, master=self.root)
        
    def poll (self):
        """polling needed for ctrl-c"""
        if self.do_draw.value != 0: # redraw
            self.app.draw()
            self.do_draw.value = 0

        self.root.pollid = self.root.after(50, self.poll)

    def run (self):
        """start polling and run application"""
        self.root.pollid = self.root.after(50, self.poll)
        self.app.mainloop()

    def stop (self):
        """stops application, called on shutdown"""
        self.root.after_cancel(self.root.pollid)
        self.root.destroy()
        self.root.quit()

# eof #

