import computer_vision as cv
import cv2
import math
import time
import os
from loguru import logger
from Communication.csv_access import save_datas

class sample:
    
    def __init__(self, num, x, y, image = None):
        self.num = num
        self.x = x
        self.y = y
        self.image = None
            
def destination(self):
    ''' Computes the destination of the tip, meaning where the tissue will be deposited, based on the current well number and the current sample number'''
    well_pos = [self.culture_well[self.well_num][0], self.culture_well[self.well_num][1]]
    
    ### Pattern 1
    match self.settings['Well']['Type']:
        case 'TPP6':
            diameter = 33.9
        case 'TPP12':
            diameter = 21
        case 'TPP24':
            diameter = 15.4
        case 'TPP48':
            diameter = 10.6
        case 'NUNC48':
            diameter = 6.4
        case 'FALCON48':
            diameter = 6.4
        case 'Millicell plate':
            diameter = 3 ### #TODO check this
        case _:
            raise ValueError('Wrong well plate type')
    radius = diameter/4 # We divide by 4, because we are defining the radius of tissue depositions, and not the radius of the well.
    if self.nb_sample == 0:
        offset = [0, 0]
    else: 
        angle = (self.nb_sample-1)*2*math.pi/(self.settings["Well"]["Number of sample per well"]-1)
        offset = [radius*math.cos(angle), radius*math.sin(angle)]
    
    ### Pattern 2
    # offset = [0, 0]
    
    # if self.nb_sample % 2 == 0: 
    #     offset[1] = 1
    # else:   
    #     offset[1] = -1
    
    # offset[0] = (self.nb_sample - 2) * 2
    
    ####
    
    return [well_pos[0]+offset[0], well_pos[1]+offset[1]]

def set_tracker(self, target_px):
    
    bbox = [int(target_px[0]-self.roi_size/2),int(target_px[1]-self.roi_size/2), self.roi_size, self.roi_size]
    self.tracker.init(self.frame, bbox)
    self.track_on = True

def release_tracker(self):
    
    self.track_on = False
    self.success = False
    self.tracker = cv2.TrackerCSRT.create()  
    
def check_pickup(self):
    ## check how this is done
    
    x, y, w, h = [int(i) for i in self.bbox]
    tracker_pos = [int(x+w/2), int(y+h/2)]
    
    if (tracker_pos[0]-self.tip_pos_px[0])**2+ (tracker_pos[1]-self.tip_pos_px[1])**2 < 20**2:
        return True
    else:
        return False
    
def check_pickup_two(self):
    
    self.macro_frame = self.stream2.read()
    
    macro_dir = r"Pictures/macro"
    
    if not os.path.exists(macro_dir):
        os.makedirs(macro_dir)
    
    _, _, files = next(os.walk(macro_dir))
    file_count = len(files)
    cv2.imwrite("Pictures/macro/macro_image_" + str(file_count) + ".png", self.macro_frame)
    #### The first line was the one being used. In the future, update the neural network by taking a series of picture, 
    #### and re-enable it instead of waiting for a user's confirmation
    # res = self.NN.predict(cv2.cvtColor(self.macro_frame, cv2.COLOR_BGR2RGB).reshape(1, 480, 640, 3), verbose=0)
    # res = self.NN.predict(cv2.cvtColor(self.macro_frame, cv2.COLOR_BGR2GRAY).reshape(1, 480, 640, 1), verbose=0)
    # logger.info(f"🔮 Prediciton results {res[0, 0]}")
    
    
    while True:      

        # Inputs
        key = cv2.waitKeyEx(5)  
        
        if key == 13: #enter
            return True
        if key == 8: #backspace
            return False
        
        self.macro_frame = self.stream2.read() 
        cv2.imshow('Macro camera', self.macro_frame) 
    # if res > 0.5:
    #     return False ## change here to take picture repeatedlz
    # else:
    #     return False
    

def delay(self, delay):

    if not self.chrono_set:
        self.chrono = delay + time.time()
        self.chrono_set = True
    elif time.time() >= self.chrono:
        self.chrono_set = False
        return True
    return False        

def detect(self):
    ''' Look at the petridish and look for tissues to pick up'''
    if self.sub_state == 'go to position':
        
        if self.com_state == 'not send':
            # self.anycubic.move_axis_relative(z=self.safe_height, f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Camera"])
            self.anycubic.move_axis_relative(x=self.detection_place[0], y=self.detection_place[1], z=self.detection_place[2], f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Camera"])
            self.anycubic.finish_request()
            self.com_state = 'send'
            
        elif self.anycubic.get_finish_flag():
            self.tip_number = 1
            self.dyna.select_tip(tip_number=self.tip_number, ID=3)
            self.sample_detector = cv.create_sample_detector(self.settings["Detection"]) 
            self.sub_state = 'analyse picture'
            self.com_state = 'not send'
            
            
    elif self.sub_state == 'analyse picture':
          
        target_px, optimal_angle = cv.detection(self)
                
        if target_px is not None:
             
            set_tracker(self, target_px)
            self.target_pos = self.cam.cam_to_platform_space(target_px, self.detection_place)
            self.offset_check = (self.dist_check*math.sin(optimal_angle), self.dist_check*math.cos(optimal_angle))

            self.state = 'pick'
            self.sub_state = 'empty pipette'
            self.com_state = 'not send'
            self.detect_attempt = 0
            out = self.frame.copy()

            macro_dir = r"Pictures/cam2"
            
            if not os.path.exists(macro_dir):
                os.makedirs(macro_dir)
            
            _, _, files = next(os.walk(macro_dir))
            file_count = len(files)
            cv2.imwrite("Pictures/cam2/successful_capture_" + str(file_count) + ".png", out)
            
        else:
            self.detect_attempt += 1
            ## Maybe add a bed shake to move the tissues around
            if self.detect_attempt == self.max_detect_attempt:
                self.state = 'pause'
                self.last_state = 'detect'
                self.detect_attempt = 0
                out = self.frame.copy()
    
                macro_dir = r"Pictures/cam2"
                
                if not os.path.exists(macro_dir):
                    os.makedirs(macro_dir)
                
                _, _, files = next(os.walk(macro_dir))
                file_count = len(files)
                cv2.imwrite("Pictures/cam2/failed_capture_" + str(file_count) + ".png", out)
                logger.info('🔎 No tissue detected')
    
def pick(self):   
    
    if self.sub_state == 'empty pipette':
    
        if self.com_state == 'not send':
            self.dyna.write_profile_velocity(self.settings["Tissues"]["Dropping speed"], ID = 1)
            self.pipette_1_pos = 310
            self.dyna.write_pipette_ul(self.pipette_1_pos, ID = 1)
            self.com_state = 'send'
            
        elif self.dyna.pipette_is_in_position_ul(self.pipette_1_pos, ID = 1):
            self.sub_state = 'go to position'
            self.com_state = 'not send'
                
            
    elif self.sub_state == 'go to position':
        
        if self.com_state == 'not send':
            self.anycubic.move_axis_relative(x=self.target_pos[0]+self.offset_check[0], y=self.target_pos[1]+self.offset_check[1], z=self.settings["Position"]["Pick height"] + self.pick_offset, f=self.settings["Speed"]["Medium speed"], offset=self.settings["Offset"]["Tip one"])
            self.anycubic.finish_request()
            self.com_state = 'send'
            
        elif self.anycubic.get_finish_flag():
            self.sub_state = 'correction'
            self.com_state = 'not send'
            

    elif self.sub_state == 'correction':
        
        if self.com_state == 'not send':
            if delay(self, 0.3):
                x, y, w, h = self.bbox
                target_px = [int(x+w/2), int(y+h/2)]
                cam_pos = (self.target_pos[0]+self.offset_check[0]-self.settings["Offset"]["Camera"][0]+self.settings["Offset"]["Tip one"][0], self.target_pos[1]+self.offset_check[1]-self.settings["Offset"]["Camera"][1]+self.settings["Offset"]["Tip one"][1], self.settings["Position"]["Pick height"] + self.pick_offset-self.settings["Offset"]["Camera"][2]+self.settings["Offset"]["Tip one"][2])
                self.target_pos = self.cam.cam_to_platform_space(target_px, cam_pos)
                if (self.target_pos[0]-self.petridish_pos[0])**2+(self.target_pos[1]-self.petridish_pos[1])**2 > self.petridish_radius**2:
                    self.state = 'reset'
                    self.sub_state = 'go to position'
                    self.com_state = 'not send'         
                    self.pick_attempt = 0    
                else:              
                    man_corr = [0., 1.0] # Small manual offset to correct dynamic offset
                    self.anycubic.move_axis_relative(x=self.target_pos[0]+man_corr[0], y=self.target_pos[1]+man_corr[1], z=self.settings["Position"]["Pick height"], f=self.settings["Speed"]["Slow speed"], offset=self.settings["Offset"]["Tip one"])
                    # indirect move to go on top
                    # self.anycubic.move_axis_relative(x=self.target_pos[0], y=self.target_pos[1], z=self.settings["Position"]["Pick height"]+2, f=self.settings["Speed"]["Slow speed"])
                    # self.anycubic.move_axis_relative(z=self.settings["Position"]["Pick height"], f=self.settings["Speed"]["Slow speed"])
                    self.anycubic.finish_request()
                    self.com_state = 'send'
        
        elif self.anycubic.get_finish_flag():
            self.sub_state = 'suck'
            self.com_state = 'not send'
    

    elif self.sub_state == 'suck':
        
        if self.com_state == 'not send':
            self.pipette_1_pos = self.pipette_1_pos - self.settings["Tissues"]["Pumping Volume"]
            self.dyna.write_profile_velocity(self.settings["Tissues"]["Pumping speed"], ID = 1)
            self.dyna.write_pipette_ul(self.pipette_1_pos, ID = 1)
            self.com_state = 'send'
            
        elif self.dyna.pipette_is_in_position_ul(self.pipette_1_pos, ID = 1):
            self.sub_state = 'check'
            self.com_state = 'not send'
            
    
    elif self.sub_state == 'check':
        
        if self.com_state == 'not send':
            self.anycubic.move_axis_relative(z=self.settings["Position"]["Pick height"] + self.pick_offset, f=self.settings["Speed"]["Slow speed"], offset=self.settings["Offset"]["Tip one"])
            self.anycubic.move_axis_relative(x=self.target_pos[0]+self.offset_check[0], y=self.target_pos[1]+self.offset_check[1], f=self.settings["Speed"]["Slow speed"], offset=self.settings["Offset"]["Tip one"])
            self.anycubic.finish_request()
            self.com_state = 'send'
            
        elif self.anycubic.get_finish_flag():
            
            # print(check_pickup(self))
            self.pick_attempt += 1
            print(self.pick_attempt, self.settings["Detection"]["Max attempt"])
            
            if check_pickup(self): 
                release_tracker(self)
                self.state = 'picture'
                self.sub_state = 'go to position'
                self.com_state = 'not send' 
                self.pick_attempt = 0
                
            elif self.pick_attempt >= self.settings["Detection"]["Max attempt"]:
                self.state = 'reset'
                self.sub_state = 'go to position'
                self.com_state = 'not send'
                self.pick_attempt = 0 
                
            else:
                self.sub_state = 'correction'
                self.com_state = 'not send' 
                  
                
def picture(self):
    
    if self.sub_state == 'go to position':
        
        if self.com_state == 'not send':
            dest = destination(self)
            self.anycubic.move_axis_relative(z=self.safe_height, f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip one"])
            if dest[1] > 100:
                self.anycubic.move_axis_relative(x=self.picture_pos, y=100, f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip one"])
            else:
                self.anycubic.move_axis_relative(x=self.picture_pos, y=dest[1], f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip one"])
            
            self.anycubic.set_position(x=-self.x_firmware_limit_overwrite) 
            self.anycubic.move_axis_relative(x=self.picture_pos, offset=self.settings["Offset"]["Tip one"])
            self.anycubic.finish_request()
            self.com_state = 'send'
            
        elif self.anycubic.get_finish_flag():
            
            
            if delay(self, 0.5):
                
                self.pause()
                if check_pickup_two(self):
                    
                    self.state = 'place'
                    self.place_attempt = 0
                   
                else:
                    self.state = 'reset'
                
                self.sub_state = 'go to position'
                self.com_state = 'not send' 
                self.anycubic.move_axis_relative(x = -self.x_firmware_limit_overwrite)
                self.anycubic.set_position(x = 0)   
                
def place(self):

    if self.sub_state == 'go to position':
        
        if self.com_state == 'not send':
            self.anycubic.move_axis_relative(z=self.safe_height, f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip one"])
            dest = destination(self)
            if dest[1] > 100:
                self.anycubic.move_axis_relative(x=80, y=100, f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip one"])
            self.anycubic.move_axis_relative(x=dest[0], y=dest[1], f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip one"])
            self.anycubic.finish_request()
            self.com_state = 'send'
            
        elif self.anycubic.get_finish_flag():
            self.sub_state = 'go down'
            self.com_state = 'not send'       
                        
    
    elif self.sub_state == 'go down':
        
        if self.com_state == 'not send':
            self.anycubic.move_axis_relative(z=self.settings["Position"]["Drop height"], f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip one"])
            self.anycubic.finish_request()
            self.com_state = 'send'
            
        elif self.anycubic.get_finish_flag():
            self.sub_state = 'blow'
            self.com_state = 'not send'   
            
            
            
    elif self.sub_state == 'blow':
        
        if self.com_state == 'not send':
            self.dyna.write_profile_velocity(self.settings["Tissues"]["Dropping speed"], ID = 1)
            self.pipette_1_pos = self.pipette_1_pos + self.settings["Tissues"]["Dropping volume"]
            self.dyna.write_pipette_ul(self.pipette_1_pos, ID = 1)
            self.place_attempt += 1
            self.com_state = 'send'
            
        elif self.dyna.pipette_is_in_position_ul(self.pipette_1_pos, ID = 1):
            self.sub_state = 'go up'
            self.com_state = 'not send'     


    elif self.sub_state == 'go up':
        
        if self.com_state == 'not send':
            self.anycubic.move_axis_relative(z=self.safe_height, f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip one"])
            self.anycubic.finish_request()
            self.com_state = 'send'
        
        elif self.anycubic.get_finish_flag():
            self.state = 'second picture'
            self.sub_state = 'go to position'
            self.com_state = 'not send'   
            
def second_picture(self):
    
    if self.sub_state == 'go to position':
        
        if self.com_state == 'not send':
            dest = destination(self)
            self.anycubic.move_axis_relative(z=self.safe_height, f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip one"])
            if dest[1] > 100:
                self.anycubic.move_axis_relative(x=80, y=100, f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip one"])
            self.anycubic.move_axis_relative(x=self.picture_pos, f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip one"])
            
            self.anycubic.set_position(x=-self.x_firmware_limit_overwrite) 
            self.anycubic.move_axis_relative(x=self.picture_pos, offset=self.settings["Offset"]["Tip one"])
            self.anycubic.finish_request()
            self.com_state = 'send'
            
        elif self.anycubic.get_finish_flag():
            
            # print(check_pickup_two(self))
            if delay(self, 1.5):
                if check_pickup_two(self):
                    if self.place_attempt >= self.settings["Detection"]["Max place attempts"]:
                        self.state = 'reset'
                    else:
                        self.state = 'place'
                    
                else:
                    self.nb_sample += 1
                    self.state = 'reset'
                self.sub_state = 'go to position'
                self.com_state = 'not send'
                self.anycubic.move_axis_relative(x = -self.x_firmware_limit_overwrite)
                self.anycubic.set_position(x = 0)              
              
def reset(self):
    
    if self.sub_state == 'go to position':
        
        if self.com_state == 'not send':
            release_tracker(self)
            self.anycubic.move_axis_relative(z=self.safe_height, f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip one"])
            self.anycubic.move_axis_relative(x=self.reset_pos[0], y=self.reset_pos[1], f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip one"])
            self.anycubic.move_axis_relative(z=self.reset_pos[2], f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip one"]) 
            self.anycubic.finish_request() 
            self.com_state = 'send'  
            
        elif self.anycubic.get_finish_flag():
            self.sub_state = 'empty pipette'
            self.com_state = 'not send'
            
            
    elif self.sub_state == 'empty pipette':
        
        if self.com_state == 'not send':
            self.dyna.write_profile_velocity(self.settings["Tissues"]["Dropping speed"], ID = 1)
            self.pipette_1_pos = self.pipette_empty
            self.dyna.write_pipette_ul(self.pipette_1_pos, ID = 1)
            self.com_state = 'send'
            
        elif self.dyna.pipette_is_in_position_ul(self.pipette_1_pos, ID = 1):
            if self.nb_sample >= self.settings["Well"]["Number of sample per well"]:
                self.well_num += 1
                self.nb_sample = 0
                
                if self.well_num >= len(self.culture_well) or self.well_num >= self.settings["Well"]["Number of well"]:
                    self.state = 'done'
                    self.com_state = 'not send'
                else:
                    self.state = 'after wash'
                    self.sub_state = 'go to wash'
                    self.com_state = 'not send' 
            else:
                self.state = 'detect'
                self.sub_state = 'go to position'
                self.com_state = 'not send'
    
    
def after_wash(self):
    ''' After placing the sample, we need to wash the pipette before proceeding to the next sample'''
    if self.sub_state == 'go to wash':
        if self.com_state == 'not send':
            ''' Moves up (z) to a safe position, as to not break anything, moves to the washing vial, and finally enters'''
            self.anycubic.move_axis_relative(z=self.solution_well['Washing'][2], f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip one"])
            self.anycubic.move_axis_relative(x=self.solution_well['Washing'][0], y=self.solution_well['Washing'][1], f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip one"])
            self.anycubic.move_axis_relative(z=self.settings["Gel"]["Vial pumping height"], f=self.settings["Speed"]["Slow speed"], offset=self.settings["Offset"]["Tip one"]) 
            self.anycubic.finish_request() 
            self.com_state = 'send'  
        elif self.anycubic.get_finish_flag():
            ''' Waits until the movement is done, then changes the substate to wash up and sets the wash counter to 0'''
            self.wash = 0
            self.sub_state = 'wash up'
            self.com_state = 'not send'
        
        
    elif self.sub_state == 'wash up':
        ''' Pumps the washing solution from the washing vial'''
        if self.com_state == 'not send':
            ''' First sets the speed for the pumping, then pumps out the washing solution'''
            self.dyna.write_profile_velocity(self.settings["Solution B"]["Solution B pumping speed"], ID = 1)
            self.pipette_1_pos = self.pipette_full
            self.dyna.write_pipette_ul(self.pipette_1_pos, ID = 1)
            self.com_state = 'send'  
            
        elif self.dyna.pipette_is_in_position_ul(self.pipette_1_pos, ID = 1):
            ''' Waits until the pumping is done, then changes the substate to wash down and increment the wash counter'''
            self.wash += 1
                
            self.sub_state = 'wash down'
            self.com_state = 'not send'
            
            
    elif self.sub_state == 'wash down':
        ''' Pumps out washing solution from the washing vial'''
        if self.com_state == 'not send':
            ''' First sets the speed for the pumping, then pumps out the washing solution '''
            self.dyna.write_profile_velocity(self.settings["Solution B"]["Solution B pumping speed"], ID = 1)
            self.pipette_1_pos = self.pipette_empty
            self.dyna.write_pipette_ul(self.pipette_1_pos, ID = 1)
            self.com_state = 'send'  
            
        elif self.dyna.pipette_is_in_position_ul(self.pipette_1_pos, ID = 1):
            ''' Waits until the pumping is done, then changes the substate to wash up or exit vial, depending on the number of wash'''
            if self.wash >= self.settings["Gel"]["Number of wash"]:
                self.sub_state = 'exit vial'
                self.com_state = 'not send'        
                ##### is a wait necessary here?       
            else:     
                self.sub_state = 'wash up'
                self.com_state = 'not send'     
        
        
    elif self.sub_state == 'exit vial':
        ''' Self explanatory'''
        if self.com_state == 'not send':
            self.anycubic.move_axis_relative(z=self.solution_well['Washing'][2], f=self.settings["Speed"]["Fast speed"], offset=self.settings["Offset"]["Tip one"])
            self.anycubic.finish_request()
            self.com_state = 'send'
        
        if self.anycubic.get_finish_flag():
            ''' Waits until the movement is done, then changes the sub state to either preparing gel if we have to do that, or detect to continue the
            detection process. '''    
            if self.settings["Well"]["Well preparation"]:
                self.state = 'preparing gel'
            else:
                self.state = 'detect'
            self.sub_state = 'go to position'
            self.com_state = 'not send'           
                
def done(self):
    
    if self.com_state == 'not send':
        self.anycubic.move_axis_relative(z=self.safe_height, printMsg=False, offset=self.settings["Offset"]["Tip one"])
        self.anycubic.move_axis_relative(x=2200, y=220, printMsg=False, offset=self.settings["Offset"]["Tip one"])
        self.tip_number = 1
        self.dyna.select_tip(tip_number=self.tip_number, ID=3)
        logger.info('🦾 Done')
        self.com_state = 'send'  