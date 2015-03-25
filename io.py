#!/usr/bin/python3
# coding=utf-8

# Playground for Pi
# Enable/Disable some ports with LEDs and a Buzzer
# Version 0.1

import getpass
import sys
import RPi.GPIO as io

pin_buzzer     =  7

pin_led_red    = 12
pin_led_green  = 16
pin_led_blue   = 18
pin_led_yellow = 22
pin_led_white  = 11
led_patterns   = [[pin_led_red, pin_led_green, pin_led_blue, pin_led_yellow, pin_led_white],
                  [pin_led_white, pin_led_yellow, pin_led_blue, pin_led_green, pin_led_red]]


################################################################################
# Help #########################################################################
def Help():
   print('Verfügbare Kommandos:')
   print('  Hilfe')
   print('  Summer     <ein|aus>')
   print('  LED Rot    <ein|aus>')
   print('  LED Grün   <ein|aus>')
   print('  LED Blau   <ein|aus>')
   print('  LED Gelb   <ein|aus>')
   print('  LED Weiß   <ein|aus>')
   print('  Muster     <ID> <ms>')
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
   io.setup(pin_led_white,io.OUT)
   Log('Initializing done.')


################################################################################
# Buzzer #######################################################################
def Buzzer(switch):
   Log('Buzzer: {} {}'.format(pin_buzzer, switch))
   io.output(pin_buzzer,switch)


################################################################################
# Light ########################################################################
def Light(led, switch):
   Log('LED: {} {}'.format(led, switch))
#   io.output(led,switch)
   Log('Light off for safety')


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

      if (cmd[0] == '?') or (cmd[0] == 'help') or (cmd[0] == 'hilfe'): 
         Help()
         continue
      elif (cmd[0] == 'e') or (cmd[0] == 'q') or (cmd[0] == 'end') or (cmd[0] == 'ende'):
         break

      actor = cmd[0]
      if (actor == 'summer'):
         if (len(cmd) == 2):
            switch = cmd[1]
            if (switch == 'ein') or (switch == 'aus'):
               switch = GetIOConst(switch)
               Buzzer(switch)
            else:
               Help()
         else:
            Help()
         continue

      if (actor == 'led'):
         if (len(cmd) == 3):
            light  = cmd[1]
            switch = cmd[2]
            if (switch == 'ein') or (switch == 'aus'):
               switch = GetIOConst(switch)

               if (light == 'rot'):
                  Light(pin_led_red,switch)
               elif (light == 'grün'):
                  Light(pin_led_green,switch)
               elif (light == 'blau'):
                  Light(pin_led_blue,switch)
               elif (light == 'gelb'):
                  Light(pin_led_yellow,switch)
               elif (light == 'weiß'):
                  Light(pin_led_white,switch)
               else:
                  Help()
            else:
               Help()
         else:
            Help()
         continue

      if (actor == 'muster'):
         print ("Muster")
         continue


      Help()




try:
   CheckUser()
   Init()
   Main()
finally:
   Exit()

