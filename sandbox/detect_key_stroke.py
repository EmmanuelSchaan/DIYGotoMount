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
'''
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
'''

####################################################
# copied from Stack overflow, but doesn't seem to work
# maybe only works on Windows

'''
import ctypes
libX11    = ctypes.CDLL('libX11.so')
XGrabKey = libX11.XGrabKey
XGrabKeyboard = libX11.XGrabKeyboard
print("XGrabKey: "     , dir(XGrabKey))
print("XGrabKeyboard: ", dir(XGrabKeyboard))
'''

'''
import pythoncom, pyHook

def OnKeyboardEvent(event):
    print('MessageName:',event.MessageName)
    print('Message:',event.Message)
    print('Time:',event.Time)
    print('Window:',event.Window)
    print('WindowName:',event.WindowName)
    print('Ascii:', event.Ascii, chr(event.Ascii))
    print('Key:', event.Key)
    print('KeyID:', event.KeyID)
    print('ScanCode:', event.ScanCode)
    print('Extended:', event.Extended)
    print('Injected:', event.Injected)
    print('Alt', event.Alt)
    print('Transition', event.Transition)
    print('---')

# return True to pass the event to other handlers
    return True

# create a hook manager
hm = pyHook.HookManager()
# watch for all mouse events
hm.KeyDown = OnKeyboardEvent
# set the hook
hm.HookKeyboard()
# wait forever
pythoncom.PumpMessages()
'''

'''
from pyHook import HookManager
from win32gui import PumpMessages, PostQuitMessage

class Keystroke_Watcher(object):
    def __init__(self):
        self.hm = HookManager()
        self.hm.KeyDown = self.on_keyboard_event
        self.hm.HookKeyboard()


    def on_keyboard_event(self, event):
        try:
            if event.KeyID  == keycode_youre_looking_for:
                self.your_method()
        finally:
            return True

    def your_method(self):
        pass

    def shutdown(self):
        PostQuitMessage(0)
        self.hm.UnhookKeyboard()


watcher = Keystroke_Watcher()
PumpMessages()
'''


####################################################
# Reading the file in /dev/input/
# This works perfectly, even when the terminal is in the background!!!
# Sometimes, the keyboard appears as several devices; in that case, 
# not all of them will allow detection when the terinal is not active,
# and I need to select hte correct one.

import evdev

devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
for device in devices:
   print(device.path, device.name, device.phys)


#device = evdev.InputDevice('/dev/input/event1')
device = evdev.InputDevice('/dev/input/event0')
print(device)

for event in device.read_loop():
   if event.type == evdev.ecodes.EV_KEY:
      print(evdev.categorize(event))

