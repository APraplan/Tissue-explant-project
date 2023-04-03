import numpy as np
import Platform.computer_vision as cv
import cv2
import threading as th
from time import sleep
from Platform.parameters import *

# PETRI_DISH_HEIGHT = 25
# PETRI_DISH_PICK_HEIGHT = 0.8
# PETRI_DISH_X_POSITION = 50
# PETRI_DISH_Y_POSITION = 100
# PETRI_DISH_RADIUS = 45

# TEST_TUBE_HEIGHT = 10
# TEST_TUBE_PLACE_HEIGHT = 3
# TEST_TUBE_X_POSITION = 180
# TEST_TUBE_Y_POSITION = 160
# TEST_TUBE_X_MIN = 105
# TEST_TUBE_X_MAX = 195
# TEST_TUBE_Y_MIN = 45
# TEST_TUBE_Y_MAX = 175
# NUMBER_TUBE_X = 8
# NUMBER_TUBE_Y = 12
# OFFSET_TUBE = 8.2


# TEST_TUBE_N = np.array([1, 0, 0])
# TEST_TUBE_P0 = np.array([TEST_TUBE_X_MIN, 0, 0])

from Platform.platform_private import reset, detect, pick, place 

class platform_pick_and_place:
    
    def __init__(self, anycubic, dynamixel, detector):
        
        self.state = RESET
        
        # Picking zone
        self.safe_height = 25
        self.pick_height = 1.8
        self.detection_place = [75, 120, 50]
        self.reset_pos = [50, 100, 10]
                
        # Dropping zone
        self.dropping_pos = [180, 160]
        self.nb_pos = [8, 12]
        self.offset_pos = 8.2
        self.drop_height = 1
        
        # Anycubic
        self.anycubic = anycubic
        self.fast_speed = 4000
        self.medium_speed = 2000
        self.slow_speed = 300
        
        # Dynamixel
        self.dyna = dynamixel
        self.pipette_empty_speed = 100
        self.pipette_fill_speed = 10
        
        # Tissues
        self.nb_sample = 0
        self.sample_list = []
        
        # Camera
        self.detector = detector 
        self.mask = cv.create_mask(200, (480, 640), (320, 240))
        self.detect_attempt = 0
        self.max_attempt = 50
        self.frame = np.zeros((480, 640))
        
             
    # Private methodes
    
    def __platform_homing(self):
        
        # Home position for the printer
        self.anycubic.connect()
        self.anycubic.homing()
        self.anycubic.set_home_pos(x=0, y=200, z=0)
        self.anycubic.move_speed(speed=100)
        
        # anycubic.max_x_feedrate(15000)
        # anycubic.max_y_feedrate(15000)
        # anycubic.max_z_feedrate(100)
        
        # anycubic.move_home()
        
        # Home position for the dynamixel
        self.dyna.begin_communication()
        self.dyna.set_operating_mode("position", ID=1)
        self.dyna.write_position(self.dyna.pipette(0), ID=1)
                      
    
    def __run(self):
        
        while True:
                
            if self.state == DETECT:
                detect(self=self)
                
            elif self.state == PICK:
                pick(self=self)
                
            elif self.state == PLACE:
                place(self=self)           
                
            elif self.state == RESET:
                reset(self=self)  
                
            sleep(0.05)
            
            
    def __user_IO(self):
        
            
        while True:
            
            _, self.frame = self.cap.read() 
            
            
            # Display   
            imshow = self.print(self.frame)   
            cv2.imshow('Camera', imshow) 

            # Inputs
            key = cv2.waitKey(10) & 0xFF
            
            self.command(key)
                
            
    # Public methodes
    def start(self):
        
        self.cap = cv2.VideoCapture(0) 

        # Check if camera opened successfully
        if not self.cap.isOpened():
            print("Error opening video stream or file")
        
        self.__platform_homing()
        
        self.__thread_run = th.Thread(target=self.__run)
        self.__thread_IO = th.Thread(target=self.__user_IO)
        self.__thread_run.start()
        self.__thread_IO.start()
     
     
    def pause(self):
        pass
        
            
    def resume(self):
        pass
                

    def reset(self):
        
        # if self.state != 'reset':
            self.state = RESET
            
            
    def get_sample(self):
        
        return self.sample_list, self.nb_sample
    
    
    def print(self, image):
        
        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 0.8
        color = (255, 255, 255) #BGR
        thickness = 2
        
        # Print state
        if self.state == RESET:
            text = 'Reset'
        elif self.state == PICK:
            text = 'Pick'
        elif self.state == PLACE:
            text = 'Place'
        elif self.state == DETECT:
            text = 'Detect'
        elif self.state == PAUSE:
            text = 'Pause'
        else:
            text = 'Unknown state'
            
        position = (20, 20)
        # size, _ = cv2.getTextSize(text, font, fontScale, thickness)
        out = cv2.putText(image, text, position, font, 
                   fontScale, color, thickness, cv2.LINE_AA)    
        
        return out
    
    
    def command(self, key):
        
        if key == 27: #esc
            self.reset()
        if key == ord('p'):
            self.pause()
        if key == 13: # enter
            self.resume()  
