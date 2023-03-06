import keyboard
from pick_and_place_cinematic import *
from movement_functions import *

def select_mode():
    
    print('Press "enter" to start')
    #print('Press "m" for manual control')
    print('Press "esc" to quit')
    
    while True:
        
        if keyboard.is_pressed('enter'):
            pick_and_place()
            
            print('Press "enter" to start')
            #print('Press "m" for manual control')
            print('Press "esc" to quit')
            
        if keyboard.is_pressed('m'):
            manual_control()
            
            print('Press "enter" to start')
            #print('Press "m" for manual control')
            print('Press "esc" to quit')
            
        if keyboard.is_pressed('esc'):
            break