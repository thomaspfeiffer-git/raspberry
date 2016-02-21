#!/usr/bin/python3
# -*- coding: utf-8 -*-
###############################################################################
# test_tkinter.py                                                             #
# (c) https://github.com/thomaspfeiffer-git 2016                              #
###############################################################################
"""Some playing aroung with tkinter"""

# export DISPLAY=:0.0

import glob
import os
import time
from tkinter import *
import tkinter.font as tkf
import subprocess
import sys


PATH='/media/pi/kamera/DCIM/101VTECH/'
AVI='/media/pi/kamera/DCIM/101VTECH/*.AVI'



def Mount():
    cp = subprocess.call(["sudo", "mount", "--read-only", "/dev/sda1", "/media/pi/kamera"])

def Unmount():
    cp = subprocess.call(["sudo", "udisks", "--unmount", "/dev/sda1"])
    cp = subprocess.call(["sudo", "udisks", "--eject", "/dev/sda"])


def Load():
    EmptyListbox()
    Mount()
    FillListbox()


def Play():
    i = listbox.curselection()
    if i is not ():
        filename = listbox.get(i).split(":")[0]
        fullfilename = "%s%s" % (PATH, filename)
        returncode = subprocess.call(["mplayer", "-fs", fullfilename])


def Eject():
    EmptyListbox()
    Unmount()


def FillListbox():
    for filename in glob.iglob(AVI):
        filetime = os.path.getmtime(filename)
        (_, filename) = os.path.split(filename)
        listbox.insert(END, "%s: %s" % (filename, time.ctime(filetime)))

def EmptyListbox():
    listbox.delete(0, END)


def Exit():
    Eject()
    w.quit()
    sys.exit()


def Shutdown():
    pass




w = Tk()
w.protocol('WM_DELETE_WINDOW', Exit)
w.wm_title("Timons Autokino")
btnfont = tkf.Font(family='Arial', size=20, weight='bold')
lbfont  = tkf.Font(family='Arial', size=20)




buttonframe  = Frame(w)
btn_reload   = Button(buttonframe, command=Load,     text="Load",     font=btnfont, width=10)
btn_play     = Button(buttonframe, command=Play,     text="Play",     font=btnfont, width=10)
btn_eject    = Button(buttonframe, command=Eject,    text="Eject",    font=btnfont, width=10)
btn_exit     = Button(buttonframe, command=Exit,     text="Exit",     font=btnfont, width=10)
btn_shutdown = Button(buttonframe, command=Shutdown, text="Shutdown", font=btnfont, width=10)
btn_reload.pack()
btn_play.pack()
btn_eject.pack()
btn_exit.pack()
btn_shutdown.pack()
buttonframe.pack(side=RIGHT, anchor=N)

listboxframe = Frame(w)
scrollbarx = Scrollbar(listboxframe, orient=HORIZONTAL, width=35)
scrollbary = Scrollbar(listboxframe, orient=VERTICAL, width=35)
listbox = Listbox(listboxframe, xscrollcommand=scrollbarx.set, yscrollcommand=scrollbary.set, selectmode='browse', font=lbfont)
scrollbarx.config(command=listbox.xview)
scrollbarx.pack(side=BOTTOM, fill=X)
scrollbary.config(command=listbox.yview)
scrollbary.pack(side=RIGHT, fill=Y)
FillListbox()
listbox.pack()
listboxframe.pack(side=LEFT)


w.mainloop()



