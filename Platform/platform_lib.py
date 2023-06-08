import numpy as np
import cv2
from loguru import logger
import computer_vision as cv
from platform_private_sample import *
from platform_private_gel import *
from platform_private_gui import *

debug = False

if debug:
    from Communication.fake_communication import *
else:
    from vidgear.gears import VideoGear
    from Communication.dynamixel_controller import *
    from Communication.printer_communications import *


class platform_pick_and_place:
    
    def __init__(self, com_printer, com_dynamixel, cam_head, cam_macro):
        
        # Temp
        self.save = 0
        self.counter = 0
        self.record = True

        # FSM
        self.chrono_set = False
        self.chrono = 0
        self.state = 'pause'
        self.last_state = 'homming'
        self.sub_state = 'go to position'
        self.com_state = 'not send'
        self.calibration_point = [35, 75, 0]
        
        # Picking zone
        self.safe_height = 25
        self.pick_offset = 4
        self.detection_place = [75.0, 125, 65]
        self.reset_pos = [60, 135, 10]
        self.pipette_pos_px = [272, 390]
        self.petridish_pos = [60, 145]
        self.petridish_radius = 45
        self.pick_attempt = 0
        # self.max_attempt = 4
                
        # Dropping zone
        self.tube_num = 0
        
        # Anycubic
        self.anycubic = Printer(descriptive_device_name="printer", port_name=com_printer, baudrate=115200)
        
        # Dynamixel
        self.dyna = Dynamixel(ID=[1,2,3], descriptive_device_name="XL430 test motor", series_name=["xl", "xl", "xl"], baudrate=57600,
                 port_name=com_dynamixel)

        self.tip_number = 1
        self.pipette_1_pos = 0
        self.pipette_2_pos = 0
        self.pipette_full = 0
        self.pipette_empty = 625
        
        # Tissues
        self.target_pos = (0,0)
        self.nb_sample = 0
        
        # Camera 1 
        options = {
            "CAP_PROP_FRAME_WIDTH": 1280,
            "CAP_PROP_FRAME_HEIGHT": 720,
            "CAP_PROP_FPS": 30,
        }
        self.stream1 = VideoGear(source=cam_head, logging=True, **options).start() 
        frame = self.stream1.read() 
        self.cam = cv.Camera(frame)
        self.frame = self.cam.undistort(frame)
        self.invert = cv.invert(self.frame)
        self.mask = cv.create_mask(200, self.frame.shape[0:2], (self.frame.shape[1]//2, self.frame.shape[0]//2))
        self.intruder_detector = cv.create_intruder_detector()
        self.min_radius = 15
        self.max_radius = 38
        self.detect_attempt = 0
        self.max_detect_attempt = 50
        
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
        self.dist_check = 5
        
        # Well plate
        self.solution_prep_num = 0
        self.well_num = 0
        self.mix = 0
        self.wash = 0

        well_type = '12'
        self.mixing_well = [tube('A'), tube('B'), tube('C'), tube('D'), tube('E'), tube('F')]
        self.culture_well = [well_plate('A1', well_type), well_plate('A2', well_type), well_plate('A3', well_type), well_plate('B1', well_type), well_plate('B2', well_type), well_plate('B3', well_type)]
        self.solution_well = {'Sol A' : vial('A'), 'Sol B' : vial('B'), 'Washing' : well_plate('A4', well_type), 'Dump' : well_plate('A2', well_type)}
        
        load_parameters(self)

    # Public methodes
    
    def init(self):        
        
        self.anycubic.connect()
        self.anycubic.homing()
        # self.anycubic.set_home_pos(x=0, y=0, z=0)
        self.anycubic.max_x_feedrate(300)
        self.anycubic.max_y_feedrate(300)
        self.anycubic.max_z_feedrate(25)
        
        self.dyna.begin_communication()
        self.dyna.set_operating_mode("position", ID="all")
        self.dyna.write_profile_velocity(100, ID="all")
        self.dyna.set_position_gains(P_gain = 2700, I_gain = 50, D_gain = 5000, ID=1)
        self.dyna.set_position_gains(P_gain = 2700, I_gain = 90, D_gain = 5000, ID=2)
        self.dyna.set_position_gains(P_gain = 2500, I_gain = 40, D_gain = 5000, ID=3)
        self.tip_number = 1
        self.dyna.select_tip(tip_number=self.tip_number, ID=3)

        # self.anycubic.move_home()
        
        
    def disconnect(self):
        
        self.anycubic.disconnect()
        self.dyna.end_communication()
        
        save_parameters(self)    
        print(goodbye)
    
    
    def calibrate(self):
        
        # Macro camera calibration
        self.anycubic.move_axis(z=self.safe_height, printMsg=False)
        self.anycubic.move_axis(x=self.picture_pos, printMsg=False)
        
        while True:
        
            self.macro_frame = self.stream2.read()            

            # Inputs
            key = cv2.waitKey(5) & 0xFF 
            
            self.calibration_process(key)
            
            if key == 13: #enter
                break
            
            cv2.imshow('Macro camera', self.macro_frame) 
            
        cv2.destroyAllWindows()  
            
            
        # Offset calibration
        self.anycubic.move_axis(z=5, printMsg=False)
        self.anycubic.move_axis(x=self.calibration_point[0]+self.offset[0],y=self.calibration_point[1]+self.offset[1], printMsg=False)
        self.anycubic.move_axis(x=self.calibration_point[0]+self.offset[0],y=self.calibration_point[1]+self.offset[1], z=self.calibration_point[2]+self.offset[2], printMsg=False)
        
        while True:
        
            frame = self.stream1.read() 
            self.frame = self.cam.undistort(frame)
            self.invert = cv.invert(self.frame)
            imshow = self.frame.copy()
            
            # self.macro_frame = self.stream2.read()
             
            # Inputs
            key = cv2.waitKey(5) & 0xFF 
            
            self.calibration_process(key)
            
            if key == 13: #enter
                break
            
            cv2.imshow('Camera', imshow) 
            
        self.anycubic.move_axis_relative(z=25, printMsg=False)
        self.anycubic.move_axis_relative(x=0, y=220, printMsg=False)
                
        cv2.destroyAllWindows()   
    
    def run(self):
        
        if self.record:
            _, _, files = next(os.walk(r"Pictures\Videos"))
            id = len(files)
            out = cv2.VideoWriter(r'Pictures\Videos\video_' + str(id) + '.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (self.frame.shape[1], self.frame.shape[0]))
           
        while True:
        
            frame = self.stream1.read() 
            self.frame = self.cam.undistort(frame)
            self.invert = cv.invert(self.frame)
            
            if self.record:
                out.write(self.frame)
            
            # self.macro_frame = self.stream2.read()
            
            self.update() 
             
            # Inputs
            key = cv2.waitKey(5) & 0xFF 
            
            if key == 27: #esc
                break
            
            imshow = display(self, key)
            
            cv2.imshow('Camera', imshow) 
            # cv2.imshow('Macro cam', self.macro_frame)
                
    
        self.stream1.stop()
        self.stream2.stop()
        if self.record:
            out.release()
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
            
        elif self.state == 'second picture':
            second_picture(self)
            
        elif self.state == 'done':
            done(self)
                   
    def pause(self):
    
        if self.state != 'pause':
            logger.info('🚦 Paused')
            self.last_state = self.state
            self.state = 'pause'
            
            
    def resume(self):
        
        if self.state == 'pause':
            logger.info('🧫 Resumed')
            self.state = self.last_state
                

    def reset(self):
        
        if not (self.state == 'homming' or self.state == 'spreading solution A' or self.state == 'preparing gel'):
        
            logger.info('⚡ Soft reset')
            self.pick_attempt = 0
            self.detect_attempt = 0
            self.state = 'reset'
            self.sub_state = 'go to position'
            self.com_state = 'not send'
        
        
    def calibration_process(self, key):
        
        incr = 0.1
                
        if key == ord('a'):
            self.offset[0] -= incr
            self.anycubic.move_axis(x=self.calibration_point[0]+self.offset[0],y=self.calibration_point[1]+self.offset[1], z=self.calibration_point[2]+self.offset[2], printMsg=False)
            
        if key == ord('d'):
            self.offset[0] += incr
            self.anycubic.move_axis(x=self.calibration_point[0]+self.offset[0],y=self.calibration_point[1]+self.offset[1], z=self.calibration_point[2]+self.offset[2], printMsg=False)
            
        if key == ord('w'):
            self.offset[1] += incr
            self.anycubic.move_axis(x=self.calibration_point[0]+self.offset[0],y=self.calibration_point[1]+self.offset[1], z=self.calibration_point[2]+self.offset[2], printMsg=False)
            
        if key == ord('s'):
            self.offset[1] -= incr
            self.anycubic.move_axis(x=self.calibration_point[0]+self.offset[0],y=self.calibration_point[1]+self.offset[1], z=self.calibration_point[2]+self.offset[2], printMsg=False)
            
        if key == ord('e'):
            self.offset[2] += incr
            self.anycubic.move_axis(x=self.calibration_point[0]+self.offset[0],y=self.calibration_point[1]+self.offset[1], z=self.calibration_point[2]+self.offset[2], printMsg=False)

        if key == ord('c'):
            self.offset[2] -= incr
            self.anycubic.move_axis(x=self.calibration_point[0]+self.offset[0],y=self.calibration_point[1]+self.offset[1], z=self.calibration_point[2]+self.offset[2], printMsg=False)
            
        if key == 13: # enter
            self.anycubic.set_home_pos(self.offset[0], self.offset[1], self.offset[2])
            
            
            