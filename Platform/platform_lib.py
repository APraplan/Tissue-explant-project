import numpy as np
import Platform.computer_vision as cv
from vidgear.gears import VideoGear
import cv2
from Platform.platform_private_sample import *
from Platform.platform_private_gel import *
from Platform.Communication.dynamixel_controller import *
from Platform.Communication.printer_communications import *


class platform_pick_and_place:
    
    def __init__(self, com_printer, com_dynamixel, cam_head, cam_macro):
        
        # Temp
        self.save = 0
        self.counter = 0
        
        # GUI
        self.gui_menu = 0
        self.gui_menu_label = np.array(['Pick height', 'Drop height', 'Slow speed', 'Medium speed',
                                        'Fast speed', 'Pumping Volume', 'Pumping speed', 'Dropping volume',
                                        'Dropping speed', 'Solution pumping height', 'Solution A pumping speed',
                                        'Solution A dropping speed', 'Solution A pumping volume', 'Solution B pumping speed',
                                        'Solution B dropping speed', 'Solution B pumping volume', 'Number of mix',
                                        'Number of wash'])

        # FSM
        self.chrono_set = False
        self.chrono = 0
        self.state = 'pause'
        self.last_state = 'homming'
        self.sub_state = 'go to position'
        self.com_state = 'not send'
        
        # Picking zone
        self.pick_height = 2.8
        self.pipette_pumping_speed = 100
        self.pipette_pumping_volume = 8
        self.safe_height = 25
        self.pick_offset = 4
        self.detection_place = [75.0, 125, 50]
        self.reset_pos = [60, 135, 10]
        self.pipette_pos_px = [172, 402]
                
        # Dropping zone
        self.drop_height = 2.6
        self.pipette_dropping_speed = 150
        self.pipette_dropping_volume = 1.5
        self.tube_num = 0
        self.dropping_pos = [160, 115]
        
        # Anycubic
        self.anycubic = Printer(descriptive_device_name="printer", port_name=com_printer, baudrate=115200)
        self.fast_speed = 5000
        self.medium_speed = 2000
        self.slow_speed = 300
        
        # Dynamixel
        self.dyna = Dynamixel(ID=[1,2,3], descriptive_device_name="XL430 test motor", series_name=["xl", "xl", "xl"], baudrate=57600,
                 port_name=com_dynamixel)

        self.tip_number = 1
        self.pipette_1_pos = 0
        self.pipette_2_pos = 0
        self.pipette_full = 0
        self.pipette_empty = 100
        
        # Tissues
        self.target_pos = (0,0)
        self.nb_sample = 0
        
        # Camera 1 
        options = {
            "CAP_PROP_FRAME_WIDTH": 1080,
            "CAP_PROP_FRAME_HEIGHT": 720,
            "CAP_PROP_FPS": 30,
        }
        self.stream1 = VideoGear(source=cam_head, logging=True, **options).start() 
        frame = self.stream1.read() 
        self.cam = cv.Camera(frame)
        self.frame = self.cam.undistort(frame)
        self.invert = cv.invert(self.frame)
        self.imshow = self.frame
        self.mask = cv.create_mask(200, self.frame.shape[0:2], (self.frame.shape[1]//2, self.frame.shape[0]//2))
        self.intruder_detector = cv.create_intruder_detector()
        self.sample_detector = cv.create_sample_detector() 
        self.min_radius = 15
        self.max_radius = 38
        self.detect_attempt = 0
        self.max_attempt = 50
        
        # Camera 2
        self.stream2 = VideoGear(source=cam_macro, logging=True).start() 
        self.macro_frame = self.stream2.read()
        self.picture_pos = 0.0
        
        # Tracker
        self.tracker = cv2.TrackerCSRT.create()       
        self.roi_size = 25
        self.track_on = False
        self.bbox = (0,0,0,0)
        self.success = False
        self.offset_check = 0
        self.dist_check = 4
        
        # Well plate
        self.solution_prep_num = 0
        self.well_num = 0
        self.solution_pumping_height = 4.0
        self.solution_A_pumping_speed = 50
        self.solution_A_dropping_speed = 35 
        self.solution_A_pumping_volume = 30
        self.solution_B_pumping_speed = 50
        self.solution_B_dropping_speed = 35
        self.solution_B_pumping_volume = 30
        self.mix = 0
        self.num_mix = 3
        self.wash = 0
        self.num_wash = 3
        self.mixing_well = [well_plate('F3'), well_plate('E3'), well_plate('D3'), well_plate('F4'), well_plate('E4'), well_plate('D4')]
        self.culture_well = [well_plate('F6'), well_plate('E6'), well_plate('D6'), well_plate('F7'), well_plate('E7'), well_plate('D7')]
        self.solution_well = {'Sol A' : well_plate('A3'), 'Sol B' : well_plate('B3'), 'Washing' : well_plate('A4'), 'Dump' : well_plate('B4')}

    
    # Public methodes
    
    def init(self):        
        
        self.dyna.begin_communication()
        self.dyna.set_operating_mode("position", ID="all")
        self.dyna.write_profile_velocity(100, ID="all")
        self.dyna.set_position_gains(P_gain = 2700, I_gain = 70, D_gain = 5000, ID=1)
        self.dyna.set_position_gains(P_gain = 2700, I_gain = 70, D_gain = 5000, ID=2)
        self.dyna.set_position_gains(P_gain = 2500, I_gain = 40, D_gain = 5000, ID=3)
        self.tip_number = 1
        self.dyna.select_tip(tip_number=self.tip_number, ID=3)
        
        self.anycubic.connect()
        self.anycubic.homing()
        # self.anycubic.set_home_pos(x=0, y=0, z=0)
        self.anycubic.max_x_feedrate(300)
        self.anycubic.max_y_feedrate(100)
        self.anycubic.max_z_feedrate(20)
        

        # self.anycubic.move_home()
        # self.dyna.write_pipette(self.pipette_empty, ID=1)
        
        
    def disconnect(self):
        
        self.anycubic.disconnect()
        self.dyna.end_communication()
        
        print_parameters(self)    
        print(goodbye)
    
    
    def run(self):
        
        # out = cv2.VideoWriter('video.mp4', -1, 25.0, (603,427))
           
        while True:
        
            frame = self.stream1.read() 
            self.frame = self.cam.undistort(frame)
            self.invert = cv.invert(self.frame)
            self.imshow = self.frame
            
            self.macro_frame = self.stream2.read()
            
            self.update() 
             
            # Inputs
            key = cv2.waitKey(10) & 0xFF    
            
            self.gui(key)
            
            if key == 27: #esc
                self.reset()
                break
            
            self.print() 
            
            cv2.imshow('Camera', self.imshow) 
            cv2.imshow('Macro cam', self.macro_frame)
                
    
        self.stream1.stop()
        self.stream2.stop()
        # out.release()
        cv2.destroyAllWindows()
        
    
    def update(self):
        
        if self.track_on:
            self.success, self.bbox = self.tracker.update(self.frame) 
            
        if self.state == 'homming':
            homming(self)
          
        elif   self.state == 'spreading solution A':
            spreading_solution_A(self)
            
        elif self.state == 'preparing gel':
            preparing_gel(self)
                        
        elif self.state == 'detect':
            detect(self)
            
        elif self.state == 'pick':
            pick(self)
            
        elif self.state == 'picture':
            picture(self)
        
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
        self.nb_sample = 0
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
        self.imshow = cv2.putText(self.imshow, text, position, font, 
                   fontScale, color, thickness, cv2.LINE_AA)    
        
        text = self.sub_state
        position = (20, 50)
        # size, _ = cv2.getTextSize(text, font, fontScale, thickness)
        self.imshow = cv2.putText(self.imshow, text, position, font, 
                   fontScale, color, thickness, cv2.LINE_AA)   
        
        text = 'Nb sample : ' + str(self.nb_sample) 
        position = (20, 80)   
        self.imshow = cv2.putText(self.imshow, text, position, font, 
                   fontScale, color, thickness, cv2.LINE_AA)
        
        if self.success:
            x, y, w, h = [int(i) for i in self.bbox]
            cv2.circle(self.imshow, (int(x+w/2), int(y+h/2)), int((w+h)/4), (255, 0, 0), 2)
            # cv2.rectangle(imshow, (x, y), (x + w, y + h), (0, 0, 255), 2)

   
    def gui(self, key):
        
        if key == ord('c'):
            cv2.imwrite("Pictures\Realsample\image_on_the_go.png", self.frame)
        
        if key == ord('p'):
            self.pause()
        if key == 13: # enter
            self.resume()
        if key == ord('r'):
            self.reset()
        
        if key == ord('a'):
            self.gui_menu += 1
            if self.gui_menu == len(self.gui_menu_label):
                self.gui_menu = 0
                
        if key == ord('d'):
            self.gui_menu -= 1
            if self.gui_menu < 0:
                self.gui_menu = len(self.gui_menu_label)-1
                
        if key == ord('w'):
            gui_parameter(self, 'up')
            
        if key == ord('s'):
            gui_parameter(self, 'down')
                        
        display(self, [20, 500])