#!/usr/bin/python
# coding=utf-8

# Playground for Pi
# Enable/Disable some ports with LEDs and a Buzzer
# Version 0.1

import getpass
import os
from time import sleep
import sys
import traceback

import RPi.GPIO as io
import dhtreader


# Actors ###################
pin_buzzer     =  7

pin_led_red    = 12
pin_led_green  = 16
pin_led_blue   = 18
pin_led_yellow = 22
pin_led_white  = 11
pin_led_bright_yellow = 19
pin_led_big    = 21
state_led_big  = io.LOW

led_patterns   = [[pin_led_green, pin_led_red, pin_led_yellow, pin_led_blue, pin_led_white,pin_led_bright_yellow],
                  [pin_led_bright_yellow,pin_led_white, pin_led_blue, pin_led_yellow, pin_led_red, pin_led_green]]

all_actors     = [pin_buzzer, \
                  pin_led_green, pin_led_red, pin_led_yellow, pin_led_blue, pin_led_white, pin_led_bright_yellow, \
                  pin_led_big]


# Sensors ##################
pin_sensor     = 15
pin_sensor_bcm = 22

pin_reed       = 23



################################################################################
# Help #########################################################################
def Help():
   print('Verfügbare Kommandos:')
   print('  Hilfe')
   print('  Summer       <ein|aus>')
   print('                        ')
   print('  LED Rot      <ein|aus>')
   print('  LED Grün     <ein|aus>')
   print('  LED Blau     <ein|aus>')
   print('  LED Gelb     <ein|aus>')
   print('  LED Weiß     <ein|aus>')
   print('  LED Hellgelb <ein|aus>')
   print('  LED groß     <ein|aus>')
   print('  Alles        <ein|aus>')
   print('                        ')
   print('  Muster       <ID> <Verzögerung [ms]> <Wiederholungen>')
   print('                        ')
   print('  Sensor                ')
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
# Light ########################################################################
def Light(led, switch):
   Log('LED: {} {}'.format(led, switch))
   io.output(led,switch)
#   Log('Light off for safety')


################################################################################
# ChangeState_LedGross #########################################################
def ChangeState_LedGross():
   global state_led_big
   if (state_led_big == io.HIGH):
      state_led_big = io.LOW
   else:
      state_led_big = io.HIGH
   Light(pin_led_big,state_led_big)


################################################################################
# ReedToggle ###################################################################
def ReedToggle(pin):
   if (io.input(pin) == False):
      ChangeState_LedGross()


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
   io.setup(pin_led_bright_yellow,io.OUT)
   io.setup(pin_led_big,io.OUT)

   io.setup(pin_reed,io.IN) 
   io.add_event_detect(pin_reed,io.BOTH)
   io.add_event_callback(pin_reed,ReedToggle)

   dhtreader.init()

   Log('Initializing done.')


################################################################################
# GetCPUTemperature ############################################################
def GetCPUTemperature():
   res = os.popen('vcgencmd measure_temp').readline()
   return(float(res.replace("temp=","").replace("'C\n","")))


################################################################################
# Buzzer #######################################################################
def Buzzer(switch):
   Log('Buzzer: {} {}'.format(pin_buzzer, switch))
   io.output(pin_buzzer,switch)


################################################################################
# Pattern ######################################################################
def Pattern(idx, delay, iterations):
   Log('Pattern: {} {}'.format(idx, delay))
   for i in range(iterations):
      print("Durchgang: {}".format(i+1))
      for led in led_patterns[idx]:
         Light(led,io.HIGH)
         sleep(delay)
         Light(led,io.LOW)


################################################################################
# AllActors ####################################################################
def AllActors(switch):
  Log('All actors: {}'.format(switch))
  for a in all_actors:
     io.output(a,switch)   # TODO Better: Light() and Buzzer()


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
   global state_led_big

   while 1:
      print('')
      cmd = raw_input("Was soll ich tun? ")

      if (len(cmd) == 0):
         Help()
         continue

      cmd = cmd.lower().split()

      if (cmd[0] in ['?', 'help', 'hilfe']):
         Help()
         continue
      elif (cmd[0] in ['e', 'q', 'end', 'ende']):
         break

      command = cmd[0]

# Summer ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
      if (command == 'summer'):
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

# LED +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
      if (command == 'led'):
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
               elif (light == 'hellgelb'):
                  Light(pin_led_bright_yellow,switch)
               elif (light == 'groß'):
                  Light(pin_led_big,switch)
                  state_led_big = switch
               else:
                  Help()
            else:
               Help()
         else:
            Help()
         continue

# Muster ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
      if (command == 'muster'):
         if (len(cmd) == 4):
            led_pattern       = cmd[1]
            led_pattern_delay = cmd[2]
            iterations        = cmd[3]
            if not led_pattern.isdigit() \
               or not led_pattern_delay.isdigit() \
               or not iterations.isdigit():
               Help()
               continue

            led_pattern = int(led_pattern)
            led_pattern_delay = float(led_pattern_delay)
            iterations  = int(iterations)
            if (led_pattern < 1) or (led_pattern > len(led_patterns)):
               Help()
               continue

            if (led_pattern_delay < 2) or (led_pattern_delay > 60000):
               Help()
               continue

            if (iterations < 1) or (iterations > 1000):
               Help()
               continue

            Pattern(led_pattern-1,led_pattern_delay/1000,iterations) 

         else:
            Help()
         continue

# All actors ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
      if (command == 'alles'):
         switch = cmd[1]
         if (switch == 'ein') or (switch == 'aus'):
            switch = GetIOConst(switch)
            AllActors(switch)
         else:
            Help()
         continue

# Sensor ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
      if (command == 'sensor'):
         i = 1
         while (i <= 5):
            try:
               print("Try #{}".format(i))
               t, h = dhtreader.read(22,pin_sensor_bcm)
            except TypeError:
               t = h = -99.99
               i += 1
               continue
            break

         CPUTemp = GetCPUTemperature()
         print("CPU Temperatur: {:.2f} °C".format(CPUTemp))
         print("Temperatur: {:.2f} °C".format(t))
         print("Luftfeuchtigkeit: {:.2f} %".format(h))
         continue

# Help ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
      Help()


################################################################################
try:
   CheckUser()
   Init()
   Main()

except:
   print(traceback.print_exc())

finally:
   Exit()

