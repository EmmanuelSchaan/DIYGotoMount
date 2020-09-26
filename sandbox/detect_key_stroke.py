# I could not get this to work: "need sudo privileges to use keyboard"
'''
import keyboard

while True:
   try:
      if keyboard.is_pressed('q'):
         print("you pressed the key q")
         break
   except:
      break
'''

####################################################
# This works at detecting key strokes,
#but only when the pygame window is active
'''
import pygame
pygame.init()

#screen = pygame.display.set_mode((400, 400))

done = False
while not done:
   
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         done = True
      elif event.type == pygame.KEYDOWN:
         if event.key == pygame.K_w:
            print("pressed w!")
'''

####################################################
# Works somewhat, but requires the terminal to be
# the active windwo
'''
import curses

# init the curse screen
stdscr = curses.initscr()

# use cbreak not to require a return key press
curses.cbreak()

print("press q to quit")

quit = False
while not quit:
   c = stdscr.getch()
   print curses.keyname(c)
   if curses.keyname(c)=='q':
      quit = True

curses.endwin()
'''

####################################################
# Using pynput: works, but only when terminal is
# the front window

from pynput.keyboard import Key, Listener
#import RPi.GPIO as GPIO
import logging
from time import sleep

# setting gpio pin for led
#GPIO.setWarnings(False)
#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(8, GPIO.OUT, intial=GPIO.LOW)

#current directory
log_dir = ""

#creating new file and setting format of everyline to be printed
logging.basicConfig(filename=(log_dir + "key_log.txt"), level=logging.DEBUG, format='%(asctime)s: %(message)s')

#add logging information before key value
def on_press(key):
    logging.info(str(key))
    #GPIO.output(8, GPIO.HIGH)
    sleep(0.05)
    #GPIO.output(8, GPIO.LOW)

#collect keys on pressed in keyboard
with Listener(on_press=on_press) as listener: 
    listener.join()

