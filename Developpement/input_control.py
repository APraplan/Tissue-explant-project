import numpy as np
import Platform.computer_vision as cv
import cv2
import threading as th
from time import sleep
import keyboard


class user_input:
    
    def __init__(self):
        self.key = 0
        
        
    # Private methodes
    def __run(self):
        
        while True:
            
            self.key = keyboard.is_pressed()           
            
            sleep(0.05)
            
    
    # Public methodes
    def start(self):
        
        self.__thread = th.Thread(target=self.__run)
        self.__thread.start()
     
     
    def is_pressed(self):
         
        return self.key