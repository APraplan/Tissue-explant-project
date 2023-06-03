import numpy as np
import Platform.computer_vision as cv
from vidgear.gears import VideoGear
import cv2
import tensorflow as tf
from keras.models import load_model
from Platform.platform_private_sample import *
from Platform.platform_private_gel import *
from Platform.platform_private_gui import *
from Platform.Communication.dynamixel_controller import *
from Platform.Communication.printer_communications import *


class platform_pick_and_place:
    
    def __init__(self, com_printer, com_dynamixel, cam_head, cam_macro):
        
        # Temp
        self.save = 0
        self.counter = 0
        self.record = True
        
        # GUI
        self.background = cv2.imread(r'C:\Users\APrap\Documents\CREATE\Pick-and-Place\Pictures\Utils\Backgroud.png')
        self.round_edges_mask = cv2.imread(r'C:\Users\APrap\Documents\CREATE\Pick-and-Place\Pictures\Utils\mask_rounded_edges.png')
        self.gui_menu = 0
        self.gui_menu_label = np.array([['Pick height', 'mm'],
                                        ['Drop height', 'mm'],
                                        ['Slow speed', 'mm/s'],
                                        ['Medium speed', 'mm/s'],
                                        ['Fast speed', 'mm/s'],
                                        ['Pumping Volume', 'ul'],
                                        ['Pumping speed', ''],
                                        ['Dropping volume', 'ul'],
                                        ['Dropping speed', ''],
                                        ['Solution pumping height', 'mm'],
                                        ['Solution A pumping speed', ''],
                                        ['Solution A dropping speed', ''],
                                        ['Solution A pumping volume', 'ul'],
                                        ['Solution B pumping speed', ''],
                                        ['Solution B dropping speed', ''],
                                        ['Solution B pumping volume', 'ul'], 
                                        ['Number of mix', ''],
                                        ['Number of wash', ''],
                                        ['Max attempt', ''],
                                        ['Well prepatation', ''],
                                        ['Number of sample per well', ''],
                                        ['Number of well', '']])

        # FSM
        self.chrono_set = False
        self.chrono = 0
        self.state = 'pause'
        self.last_state = 'homming'
        self.sub_state = 'go to position'
        self.com_state = 'not send'
        self.calibration_point = [35, 75, 0]
        # self.offset = [0.0, 0.0, 0.0]
        
        # Picking zone
        # self.pick_height = 3.1
        # self.pipette_pumping_speed = 100
        # self.pipette_pumping_volume = 8
        self.safe_height = 25
        self.pick_offset = 4
        self.detection_place = [75.0, 125, 65]
        self.reset_pos = [60, 135, 10]
        self.pipette_pos_px = [272, 390]
        self.pick_attempt = 0
        # self.max_attempt = 4
                
        # Dropping zone
        # self.drop_height = 7.0
        # self.pipette_dropping_speed = 150
        # self.pipette_dropping_volume = 1.5
        self.tube_num = 0
        self.petridish_pos = [60, 145]
        self.petridish_radius = 45
        
        # Anycubic
        self.anycubic = Printer(descriptive_device_name="printer", port_name=com_printer, baudrate=115200)
        # self.fast_speed = 5000
        # self.medium_speed = 2000
        # self.slow_speed = 350
        
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
        # self.nb_sample_well = 6
        
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
        self.sample_detector = cv.create_sample_detector() 
        self.min_radius = 15
        self.max_radius = 38
        self.detect_attempt = 0
        self.max_detect_attempt = 50
        
        # Camera 2
        self.stream2 = VideoGear(source=cam_macro, logging=True).start() 
        self.macro_frame = self.stream2.read()
        self.picture_pos = 0.0
        
        # NN
        self.NN = load_model(r'C:\Users\APrap\Documents\CREATE\Pick-and-Place\TEP_convNN_92')
        
        # Tracker
        self.tracker = cv2.TrackerCSRT.create()       
        self.roi_size = 25
        self.track_on = False
        self.bbox = (0,0,0,0)
        self.success = False
        self.dist_check = 5
        
        # Well plate
        # self.well_preparation = False
        self.solution_prep_num = 0
        self.well_num = 0
        # self.number_of_well = 6
        # self.solution_pumping_height = 4.0
        # self.solution_A_pumping_speed = 50
        # self.solution_A_dropping_speed = 35 
        # self.solution_A_pumping_volume = 30
        # self.solution_B_pumping_speed = 50
        # self.solution_B_dropping_speed = 35
        # self.solution_B_pumping_volume = 30
        self.mix = 0
        # self.num_mix = 3
        self.wash = 0
        # self.num_wash = 3
        self.mixing_well = [well_plate('F3'), well_plate('E3'), well_plate('D3'), well_plate('F4'), well_plate('E4'), well_plate('D4')]
        self.culture_well = [well_plate('F6'), well_plate('E6'), well_plate('D6'), well_plate('F7'), well_plate('E7'), well_plate('D7')]
        self.solution_well = {'Sol A' : well_plate('A3'), 'Sol B' : well_plate('B3'), 'Washing' : well_plate('A4'), 'Dump' : well_plate('B4')}
        
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
            key = cv2.waitKey(10) & 0xFF    
            
            self.calibration_process(key)
            
            if key == 13: #enter
                break
            
            
            cv2.imshow('Camera', imshow) 
            # cv2.imshow('Macro cam', self.macro_frame)
            
        self.anycubic.move_axis_relative(z=25, printMsg=False)
        self.anycubic.move_axis_relative(x=0, y=200, printMsg=False)
                
        cv2.destroyAllWindows()   
    
    def run(self):
        
        if self.record:
            _, _, files = next(os.walk(r"C:\Users\APrap\Documents\CREATE\Pick-and-Place\Pictures\Videos"))
            id = len(files)
            out = cv2.VideoWriter(r'C:\Users\APrap\Documents\CREATE\Pick-and-Place\Pictures\Videos\video_' + str(id) + '.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (self.frame.shape[1], self.frame.shape[0]))
           
        while True:
        
            frame = self.stream1.read() 
            self.frame = self.cam.undistort(frame)
            self.invert = cv.invert(self.frame)
            
            if self.record:
                out.write(self.frame)
            
            # self.macro_frame = self.stream2.read()
            
            self.update() 
             
            # Inputs
            key = cv2.waitKey(10) & 0xFF    
            
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
            
            
            