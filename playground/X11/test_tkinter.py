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


PATH='/media/pi/6464-6335/DCIM/101VTECH/'
AVI='/media/pi/6464-6335/DCIM/101VTECH/*.AVI'


def Reload():
    EmptyListbox()
    FillListbox()


def Play():
    i = listbox.curselection()
    if i is not ():
        filename = listbox.get(i).split(":")[0]
        fullfilename = "%s%s" % (PATH, filename)
        returncode = subprocess.call(["mplayer", "-fs", fullfilename])


def Eject():
    EmptyListbox()
    pass
    # sudo apt-get install eject
    # udisks --unmount /dev/sda
    # udisks --eject /dev/sda

    # $> mount
    # /dev/sda1 on /media/pi/6464-6335 type vfat (rw,nosuid,nodev,relatime,uid=1000,gid=1000,fmask=0022,dmask=0077,codepage=437,iocharset=ascii,shortname=mixed,showexec,utf8,flush,errors=remount-ro,uhelper=udisks2)
    # /dev/sdc1 on /media/pi/VT SYSTEM type vfat (rw,nosuid,nodev,relatime,uid=1000,gid=1000,fmask=0022,dmask=0077,codepage=437,iocharset=ascii,shortname=mixed,showexec,utf8,flush,errors=remount-ro,uhelper=udisks2)


def FillListbox():
    for filename in glob.iglob(AVI):
        filetime = os.path.getmtime(filename)
        (_, filename) = os.path.split(filename)
        listbox.insert(END, "%s: %s" % (filename, time.ctime(filetime)))


def EmptyListbox():
    listbox.delete(0, END)


def Exit():
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
btn_connect  = Button(buttonframe, command=Reload,   text="Reload", font=btnfont, width=10)
btn_play     = Button(buttonframe, command=Play,     text="Play", font=btnfont, width=10)
btn_eject    = Button(buttonframe, command=Eject,    text="Eject", font=btnfont, width=10)
btn_exit     = Button(buttonframe, command=Exit,     text="Exit", font=btnfont, width=10)
btn_shutdown = Button(buttonframe, command=Shutdown, text="Shutdown", font=btnfont, width=10)
btn_connect.pack()
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



