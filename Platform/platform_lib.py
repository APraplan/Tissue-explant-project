import numpy as np
import cv2
import threading
from loguru import logger
import computer_vision as cv
from platform_private_sample import *
from platform_private_gel import *
from platform_private_gui import *
from Communication.ports_gestion import *
import Developpement.Cam_gear as cam_gear


debug = False

if debug:
    from Communication.fake_communication import *
else:
    from vidgear.gears import VideoGear
    from Communication.dynamixel_controller import *
    from Communication.printer_communications import *
    import Developpement.Cam_gear as cam_gear


class platform_pick_and_place:
    
    def __init__(self):
        
        load_parameters(self)
        ###### Add comment to these parameters to make it clearer
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
        self.flag = True
        
        # Picking zone
        self.safe_height = 25
        self.pick_offset = 4
        self.detection_place = [30, 50, 65]
        self.reset_pos = [30, 50, 10]
        self.petridish_pos = [30, 50]
        self.petridish_radius = 45
        self.pick_attempt = 0
                
        # Dropping zone
        self.tube_num = 0
        
        # Anycubic
        self.anycubic = Printer(descriptive_device_name="printer", port_name=get_com_port("1A86", "7523"), baudrate=115200)
        self.x_firmware_limit_overwrite = -9
        # Dynamixel
        
        self.tip_number = 1
        self.pipette_1_pos = 0
        self.pipette_2_pos = 0
        self.pipette_full = 0
        self.pipette_empty = 575
        self.pipette_max_ul = self.pipette_empty + 100
        
        self.dyna = Dynamixel(ID=[1,2,3], descriptive_device_name="XL430 test motor", series_name=["xl", "xl", "xl"], baudrate=57600,
                pipette_max_ul= self.pipette_max_ul, port_name=get_com_port("0403", "6014")) 

        
        # Tissues
        self.target_pos = (0,0)
        self.nb_sample = 0
        
        # Camera 1 - Toolhead Camera
        self.stream1 = cam_gear.camThread("Camera 1", get_cam_index("TV Camera")) 
        self.stream1.start()
        frame = cam_gear.get_cam_frame(self.stream1)  
        self.cam = cv.Camera(frame)
        self.frame = self.cam.undistort(frame)
        self.invert = cv.invert(self.frame)
        self.mask = cv.create_mask(200, self.frame.shape[0:2], (self.frame.shape[1]//2, self.frame.shape[0]//2))
        self.intruder_detector = cv.create_intruder_detector()
        self.min_radius = 15
        self.max_radius = 38
        self.detect_attempt = 0
        self.max_detect_attempt = 50
        
        # Camera 2 - Macro Camera
        self.stream2 = cam_gear.camThread("Camera 2", get_cam_index("USB2.0 UVC PC Camera"))
        self.stream2.start()
        self.macro_frame = cam_gear.get_cam_frame(self.stream2)
        self.picture_pos = -self.settings["Offset"]["Tip one"][0]
                
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

    # Public methods
    
    def init(self):        
        ''' Initialize most of the parameters and variables. It also sends the homing command to the printer, which uses marlin firmware.'''
        self.anycubic.connect()
        
        self.dyna.begin_communication()
        self.dyna.set_operating_mode("position", ID="all")
        self.dyna.write_profile_velocity(100, ID="all")
        self.dyna.set_position_gains(P_gain = 2700, I_gain = 50, D_gain = 5000, ID=1)
        self.dyna.set_position_gains(P_gain = 2700, I_gain = 90, D_gain = 5000, ID=2)
        self.dyna.set_position_gains(P_gain = 2500, I_gain = 40, D_gain = 5000, ID=3)
        self.tip_number = 0
        self.dyna.select_tip(tip_number=self.tip_number, ID=3)
        self.dyna.write_pipette_ul(self.pipette_empty, ID=[1,2])
        
        self.anycubic.homing()
        # self.anycubic.set_home_pos(x=0, y=0, z=0)
        self.anycubic.max_x_feedrate(300)
        self.anycubic.max_y_feedrate(300)
        self.anycubic.max_z_feedrate(25)

        # Select first tip
        self.anycubic.move_axis_relative(x=15, y=0, z=self.safe_height, offset=self.settings["Offset"]["Tip one"])
        self.anycubic.finish_request()
        while not self.anycubic.get_finish_flag():
            pass
        
        

        self.tip_number = 1
        self.dyna.select_tip(tip_number=self.tip_number, ID=3)

        # self.anycubic.move_home()
        
        
    def disconnect(self):
        
        self.anycubic.disconnect()
        self.dyna.end_communication()
        
        save_parameters(self)    
        print(goodbye)
    
    
    def calibrate(self):
        ''' Starts the calibration sequence.'''
        calibration_sequence(self)
            
        self.anycubic.move_axis_relative(z=self.safe_height, offset=self.settings["Offset"]["Tip one"])
        self.anycubic.move_axis_relative(x=220, y=220, offset=self.settings["Offset"]["Tip one"])
        
        self.tip_pos_px = self.cam.platform_space_to_cam(self.settings["Offset"]["Tip one"], self.settings["Offset"]["Camera"]) + np.array([5, -5]) # small correction   
                
        cv2.destroyAllWindows()   
        
    
    def run(self):
        ''' 
        Main loop of the code.
        It will continuously run, update the pictures, and run the function update, that switches between the states
        Pressin the escape key will stop the loop and close the windows. If you close the program this way, the 
        parameters will be saved to settings.json
        '''
        if self.record:
            try :
                _, _, files = next(os.walk(r"Pictures/Videos"))
                id = len(files)
            except:
                os.makedirs(r"Pictures/Videos")
                id = 0
                
            out = cv2.VideoWriter(r'Pictures/Videos/video_' + str(id) + '.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (self.frame.shape[1], self.frame.shape[0]))

        while True:
        
            frame = cam_gear.get_cam_frame(self.stream1)  
            self.frame = self.cam.undistort(frame)
            self.invert = cv.invert(self.frame)
            
            if self.record:
                out.write(self.frame)
            
            # self.macro_frame = cam_gear.get_cam_frame(self.stream2) 
            
            self.update() 
             
            # Inputs
            key = cv2.waitKeyEx(5)

            if platform.system() == 'Linux':
                key = linux_to_windows_arrow_conversion(key)
            
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
          
        elif self.state == 'spreading solution A':
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
        '''' Should be called by pressing the button p while on the GUI '''
        if self.state != 'pause':
            logger.info('🚦 Paused')
            self.last_state = self.state
            self.state = 'pause'
            
            
    def resume(self):
        ''' Should be called by pressing the button enter while on the GUI'''
        if self.state == 'pause':
            logger.info('🧫 Resumed')
            self.state = self.last_state
        if self.state == 'Done':
            if self.settings["Well"]["Well preparation"]:
                # self.state = 'preparing gel' ## add here prep sol A
                self.state = 'spreading solution A'
            else:
                self.state = 'detect'
            self.sub_state = 'go to position'
            self.com_state = 'not send'
                

    def reset(self):
        ''' Should be called by pressing the button r while on the GUI'''
        if not (self.state == 'homming' or self.state == 'spreading solution A' or self.state == 'preparing gel'):
        
            logger.info('⚡ Soft reset')
            self.pick_attempt = 0
            self.detect_attempt = 0
            self.state = 'reset'
            self.sub_state = 'go to position'
            self.com_state = 'not send'
        
        
            
            
            