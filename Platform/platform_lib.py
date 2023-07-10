import numpy as np
import cv2
from loguru import logger
import computer_vision as cv
from platform_private_sample import *
from platform_private_gel import *
from platform_private_gui import *
from Communication.ports_gestion import *

debug = False

if debug:
    from Communication.fake_communication import *
else:
    from vidgear.gears import VideoGear
    from Communication.dynamixel_controller import *
    from Communication.printer_communications import *


class platform_pick_and_place:
    
    def __init__(self):
        
        com_ports = get_com_ports(["USB Serial Port", "USB-SERIAL CH340"])
        cam_ports = get_cam_ports(["USB2.0 UVC PC Camera", "TV Camera"])
        print(com_ports)
        print(cam_ports)
        
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
        
        # Picking zone
        self.safe_height = 25
        self.pick_offset = 4
        self.detection_place = [27.0, 71, 65]
        self.reset_pos = [27, 71, 10]
        self.pipette_pos_px = [272, 390]
        self.petridish_pos = [27, 71]
        self.petridish_radius = 45
        self.pick_attempt = 0
        # self.max_attempt = 4
                
        # Dropping zone
        self.tube_num = 0
        
        # Anycubic
        self.anycubic = Printer(descriptive_device_name="printer", port_name=com_ports.get("USB-SERIAL CH340"), baudrate=115200)
        
        # Dynamixel
        self.dyna = Dynamixel(ID=[1,2,3], descriptive_device_name="XL430 test motor", series_name=["xl", "xl", "xl"], baudrate=57600,
                 port_name=com_ports.get("USB Serial Port"))

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
        self.stream1 = VideoGear(source=cam_ports.get("TV Camera"), logging=True, **options).start() 
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
        self.stream2 = VideoGear(source=cam_ports.get("USB2.0 UVC PC Camera"), logging=True).start() 
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

        well_type = '48'
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
        self.anycubic.move_axis_relative(z=self.safe_height, offset=self.offset_tip_one)
        self.anycubic.move_axis_relative(x=self.picture_pos, offset=self.offset_tip_one)
        
        while True:
        
            self.macro_frame = self.stream2.read()            

            # Inputs
            key = cv2.waitKey(5) & 0xFF 
            
            if key == 13: #enter
                break
            
            cv2.imshow('Macro camera', self.macro_frame) 
            
        cv2.destroyAllWindows()  
            
            
        # Offset first tip calibration
        self.anycubic.move_axis_relative(z=5, offset=self.offset_tip_one)
        self.anycubic.move_axis_relative(x=0,y=0, offset=self.offset_tip_one)
        self.anycubic.move_axis_relative(z=0, offset=self.offset_tip_one)
        
        while True:
        
            frame = self.stream1.read() 
            self.frame = self.cam.undistort(frame)
            self.invert = cv.invert(self.frame)
            imshow = self.frame.copy()
            
            # self.macro_frame = self.stream2.read()
             
            # Inputs
            key = cv2.waitKey(5) & 0xFF 
            
            self.offset_tip_one = calibration_process(self, key, self.offset_tip_one)
            
            if key == 13: #enter
                print("Offset tip one: ", self.offset_tip_one)
                break
            
            cv2.imshow('Camera', imshow) 
            
            
        # Change tip
        self.anycubic.move_axis_relative(z=self.safe_height, offset=self.offset_tip_one)
        self.anycubic.finish_request()
        while not self.anycubic.get_finish_flag():
            frame = self.stream1.read() 
            self.frame = self.cam.undistort(frame)
            imshow = self.frame.copy()

            cv2.imshow('Camera', imshow) 
            
        self.tip_number = 2
        self.dyna.select_tip(tip_number=self.tip_number, ID=3)
            
              
        # Offset second tip calibration
        self.anycubic.move_axis_relative(x=0,y=0, offset=self.offset_tip_two)
        self.anycubic.move_axis_relative(z=0, offset=self.offset_tip_two)
        
        while True:
        
            frame = self.stream1.read() 
            self.frame = self.cam.undistort(frame)
            self.invert = cv.invert(self.frame)
            imshow = self.frame.copy()
            
            # self.macro_frame = self.stream2.read()
             
            # Inputs
            key = cv2.waitKey(5) & 0xFF 
            
            self.offset_tip_two = calibration_process(self, key, self.offset_tip_two)
            
            if key == 13: #enter
                print("Offset tip two: ", self.offset_tip_two)
                break
                
            cv2.imshow('Camera', imshow) 
            
        # Change tip
        self.anycubic.move_axis_relative(z=self.safe_height, offset=self.offset_tip_one)
        self.anycubic.finish_request()
        while not self.anycubic.get_finish_flag():
            frame = self.stream1.read() 
            self.frame = self.cam.undistort(frame)
            imshow = self.frame.copy()

            cv2.imshow('Camera', imshow) 
            
        self.tip_number = 1
        self.dyna.select_tip(tip_number=self.tip_number, ID=3)
            
        # Offset camera calibration
        self.anycubic.move_axis_relative(x=0,y=0, offset=self.offset_cam)
        self.anycubic.move_axis_relative(z=self.safe_height, offset=self.offset_cam)
        
        while True:
        
            frame = self.stream1.read() 
            self.frame = self.cam.undistort(frame)
            self.invert = cv.invert(self.frame)
            imshow = self.frame.copy()
            
            # self.macro_frame = self.stream2.read()
             
            # Inputs
            key = cv2.waitKey(5) & 0xFF 
            
            offset = self.offset_cam + np.array([0, 0, self.safe_height])
            offset = calibration_process(self, key, offset)
            self.offset_cam = offset - np.array([0, 0, self.safe_height])
            
            if key == 13: #enter
                print("Offset cam: ", self.offset_cam)
                break
            
            markerSize = 15
            thickness = 1
            center = (imshow.shape[1]//2, imshow.shape[0]//2)
            imshow = cv2.drawMarker(imshow, center, (255, 0, 0), cv2.MARKER_CROSS, markerSize, thickness)
            
            cv2.imshow('Camera', imshow) 

            
        self.anycubic.move_axis_relative(z=self.safe_height, offset=self.offset_tip_one)
        self.anycubic.move_axis_relative(x=0, y=220, offset=self.offset_tip_one)
                
        cv2.destroyAllWindows()   
    
    def run(self):
        
        if self.record:
            try :
                _, _, files = next(os.walk(r"Pictures\Videos"))
                id = len(files)
            except:
                os.mkdir(r"Pictures\Videos")
                id = 0
                
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
        
        
            
            
            