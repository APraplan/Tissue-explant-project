import numpy as np
import Platform.computer_vision as cv
import cv2
from Platform.platform_private import *
from Platform.Communication.dynamixel_controller import *
from Platform.Communication.printer_communications import *


class platform_pick_and_place:
    
    def __init__(self):
        self.state = 'pause'
        self.last_state = 'reset'
        self.sub_state = 'go to position'
        self.com_state = 'not send'
        
        # Picking zone
        self.safe_height = 25
        self.pick_height = 2.5
        self.pick_offset = 7
        self.detection_place = [75.0, 125, 50]
        self.reset_pos = [70, 115, 10]
        self.pipette_pos_px = [585, 468]
                
        # Dropping zone
        self.dropping_pos = [160, 115]
        # self.nb_pos = [8, 12]
        # self.offset_pos = 8.2
        self.drop_height = 2.5
        
        # Anycubic
        self.anycubic = Printer(descriptive_device_name="printer", port_name="COM10", baudrate=115200)
        self.fast_speed = 5000
        self.medium_speed = 2000
        self.slow_speed = 300
        
        # Dynamixel
        self.dyna = Dynamixel(ID=[1], descriptive_device_name="XL430 test motor", series_name=["xl"], baudrate=57600,
                 port_name="COM12")
        
        self.pipette_pos = 0
        self.pipette_full = 0
        self.pipette_empty = 100
        self.pipette_dropping_speed = 40
        self.pipette_dropping_volume = 10
        self.pipette_pumping_speed = 10
        self.pipette_pumping_volume = 20
        
        # Tissues
        self.target_pos = (0,0)
        self.nb_sample = 0
        
        # Camera
        self.cap = cv2.VideoCapture(0) 
        cv.make_720p(self.cap)  
        _, frame = self.cap.read() 
        self.cam = cv.Camera(frame)
        self.frame = self.cam.undistort(frame)
        self.mask = cv.create_mask(200, self.frame.shape[0:2], (self.frame.shape[1]//2, self.frame.shape[0]//2))
        self.detector = cv.create_detector() 
        self.detect_attempt = 0
        self.max_attempt = 50
        
        # Tracker
        self.tracker = cv2.TrackerMIL.create()       
        self.roi_size = 35
        self.track_on = False
        self.bbox = (0,0,0,0)
        self.success = False

    
    # Public methodes
    
    def init(self):
        self.anycubic.connect()
        self.anycubic.homing()
        self.anycubic.set_home_pos(x=0, y=0, z=0)
        self.anycubic.max_z_feedrate(20)
        
        self.dyna.begin_communication()
        self.dyna.set_operating_mode("position", ID=1)
        self.dyna.write_position(self.dyna.pipette(0), ID=1)
        
        
    def disconnect(self):
        
        self.anycubic.disconnect()
        self.dyna.end_communication()
    
        print('Goodbye ;)')
    
    
    def run(self):
        
        # out = cv2.VideoWriter('video.mp4', -1, 25.0, (603,427))
           
        while True:
        
            _, frame = self.cap.read() 
            self.frame = self.cam.undistort(frame)
            
      
            self.update() 
                
            # Display   
            imshow = self.print()  
             
            if self.success:
                x, y, w, h = [int(i) for i in self.bbox]
                cv2.circle(imshow, (int(x+w/2), int(y+h/2)), int((w+h)/4), (255, 0, 0), 2)
                # cv2.rectangle(imshow, (x, y), (x + w, y + h), (0, 0, 255), 2) 
                
            cv2.imshow('Camera', imshow) 
        
            # out.write(imshow)


            # Inputs
            key = cv2.waitKey(10) & 0xFF    
            
            if key == 27: #esc
                self.reset()
                break
            if key == ord('p'):
                self.pause()
            if key == 13: # enter
                self.resume()
            if key == ord('r'):
                self.track_on = False
                self.success = False
                self.tracker = cv2.TrackerMIL.create()  
            if key == ord('t'):
                x, y, w, h = [int(i) for i in self.bbox]
                print('Tracker pos :', (int(x+w/2), int(y+h/2)))
    
        self.cap.release() 
        # out.release()
        cv2.destroyAllWindows()
        
    
    def update(self):
        
        if self.track_on:
            self.success, self.bbox = self.tracker.update(self.frame) 
            
        if self.state == 'detect':
            detect(self)
            
        elif self.state == 'pick':
            pick(self)
            
        elif self.state == 'place':
            place(self)           
            
        elif self.state == 'reset':
            reset(self)  
        
     
    def pause(self):
    
        if self.state != 'pause':
            self.last_state = self.state
            self.state = 'pause'
            
            
    def resume(self):
        
        if self.state == 'pause':
            self.state = self.last_state
                

    def reset(self):
        
        # if self.state != 'reset':
            self.state = 'reset'
            self.sub_state = 'go to position'
            self.com_state = 'not send'
    
    
    def print(self):
        
        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 0.8
        color = (255, 255, 255) #BGR
        thickness = 2
        
        # Print state
        text = self.state
        position = (20, 20)
        # size, _ = cv2.getTextSize(text, font, fontScale, thickness)
        out = cv2.putText(self.frame, text, position, font, 
                   fontScale, color, thickness, cv2.LINE_AA)    
        
        text = self.sub_state
        position = (20, 50)
        # size, _ = cv2.getTextSize(text, font, fontScale, thickness)
        out = cv2.putText(self.frame, text, position, font, 
                   fontScale, color, thickness, cv2.LINE_AA)   
        
        text = 'Nb sample : ' + str(self.nb_sample) 
        position = (20, 80)   
        out = cv2.putText(self.frame, text, position, font, 
                   fontScale, color, thickness, cv2.LINE_AA)
        
        return out

   
    def gui(self):
        pass