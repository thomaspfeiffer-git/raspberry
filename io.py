#!/usr/bin/python3
# coding=utf-8

# Playground for Pi
# Enable/Disable some ports with LEDs and a Buzzer
# Version 1.0

import getpass
import sys
import RPi.GPIO as io

pin_buzzer     =  7
pin_led_red    = 12
pin_led_green  = 16
pin_led_blue   = 18
pin_led_yellow = 22


################################################################################
# Help #########################################################################
def Help():
   print('Verfügbare Kommandos:')
   print('  Hilfe')
   print('  Summer <ein|aus>')
   print('  Rot    <ein|aus>')
   print('  Grün   <ein|aus>')
   print('  Blau   <ein|aus>')
   print('  Gelb   <ein|aus>')
   print('  Ende')


################################################################################
# CheckUser ####################################################################
def CheckUser():
   if (getpass.getuser() != 'root'):
      print("Has to be run as root!")
      Exit() 


################################################################################
# Exit #########################################################################
def Exit():
   Log('Cleaning up ...')
   io.cleanup()
   sys.exit()


################################################################################
# Log ##########################################################################
def Log(l):
   print(l)


################################################################################
# Init #########################################################################
def Init():
   Log('Initializing ...')
   io.setmode(io.BOARD)
   io.setup(pin_buzzer,io.OUT)
   io.setup(pin_led_red,io.OUT)
   io.setup(pin_led_green,io.OUT)
   io.setup(pin_led_blue,io.OUT)
   io.setup(pin_led_yellow,io.OUT)
   Log('Initializing done.')


################################################################################
# Buzzer #######################################################################
def Buzzer(switch):
   Log('Summer {}'.format(switch))
   io.output(pin_buzzer,switch)


################################################################################
# Light ########################################################################
def Light(led, switch):
   Log('LED: {} {}'.format(led, switch))
   io.output(led,switch)


################################################################################
# GetIOConst ###################################################################
def GetIOConst(switch):
   if (switch == 'ein'):
      return io.HIGH
   else:
      return io.LOW                                # some kind of failsafeness #


################################################################################
# Main #########################################################################
def Main():
   while 1:
      print('')
      cmd = input("Was soll ich tun? ")

      if (len(cmd) == 0):
         Help()
         continue

      cmd = cmd.lower().split()

      switch = ''
      if (len(cmd) == 2):
         switch = cmd[1]
         if (switch != 'ein') and (switch != 'aus'):
            Help()
            continue

      if (cmd[0] == '?') or (cmd[0] == 'help') or (cmd[0] == 'hilfe'): 
         Help()
      elif (cmd[0] == 'e') or (cmd[0] == 'end') or (cmd[0] == 'ende'):
         break
      elif (switch != ''):
         switch = GetIOConst(switch)
         if (cmd[0] == 'summer'):
            Buzzer(switch)
         elif (cmd[0] == 'rot'):
            Light(pin_led_red,switch)
         elif (cmd[0] == 'grün'):
            Light(pin_led_green,switch)
         elif (cmd[0] == 'blau'):
            Light(pin_led_blue,switch)
         elif (cmd[0] == 'gelb'):
            Light(pin_led_yellow,switch)
         else:
            Help()
      else:
         Help()





try:
   CheckUser()
   Init()
   Main()
finally:
   Exit()

