import computer_vision as cv
import cv2
import math
import time
import os
import pickle

class sample:
    
    def __init__(self, num, x, y, image = None):
        self.num = num
        self.x = x
        self.y = y
        self.image = None
            
def destination(self):
    
    # mod = int(self.nb_sample/self.nb_pos[1])
    # 
    # print('Tube n° ', self.number_sample)
    # print('x offset', mod)
    # print('y offset', self.number_sample%self.num_y)
    # 
    # return round(self.dropping_pos[0]-self.offset_pos*mod, 2), round(self.dropping_pos[1]-self.offset_pos*(self.nb_sample%self.nb_pos[1]), 2)
    
    well_pos = [self.culture_well[self.well_num][0], self.culture_well[self.well_num][1]]
    
    radius = 3
    if self.nb_sample == 0:
        offset = [0, 0]
    else: 
        angle = (self.nb_sample-1)*2*math.pi/(self.nb_sample_well-1)
        offset = [radius*math.cos(angle), radius*math.sin(angle)]

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
    
    x, y, w, h = [int(i) for i in self.bbox]
    tracker_pos = [int(x+w/2), int(y+h/2)]
    
    if (tracker_pos[0]-self.pipette_pos_px[0])**2+ (tracker_pos[1]-self.pipette_pos_px[1])**2 < 20**2:
        return True
    else:
        return False
    
def check_pickup_two(self):
    
    self.macro_frame = self.stream2.read()
    
    _, _, files = next(os.walk(r"C:\Users\APrap\Documents\CREATE\Pick-and-Place\Pictures\macro"))
    file_count = len(files)
    cv2.imwrite("Pictures\macro\macro_image_" + str(file_count) + ".png", self.macro_frame)
    
    res = self.NN.predict(cv2.cvtColor(self.macro_frame, cv2.COLOR_BGR2RGB).reshape(1, 480, 640, 3))
    print(f"🔮 Prediciton results {res[0, 0]}")
    
    if res > 0.5:
        return True
    else:
        return False
    

def delay(self, delay):

    if not self.chrono_set:
        self.chrono = delay/1000.0 + time.time()
        self.chrono_set = True
    elif time.time() >= self.chrono:
        self.chrono_set = False
        return True
    return False        

def detect(self):
    

    if self.sub_state == 'go to position':
        
        if self.com_state == 'not send':
            self.anycubic.move_axis_relative(z=self.safe_height, f=self.fast_speed)
            self.anycubic.move_axis_relative(x=self.detection_place[0], y=self.detection_place[1], z=self.detection_place[2], f=self.fast_speed)
            self.anycubic.finish_request()
            self.com_state = 'send'
            
        elif self.anycubic.get_finish_flag():
            self.tip_number = 1
            self.dyna.select_tip(tip_number=self.tip_number, ID=3)
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
        else:
            self.detect_attempt += 1
            
            if self.detect_attempt == self.max_detect_attempt:
                self.state = 'pause'
                self.last_state = 'detect'
                self.detect_attempt = 0
                print('No tissue detected')
    
def pick(self):
            
    
    if self.sub_state == 'empty pipette':
    
        if self.com_state == 'not send':
            self.dyna.write_profile_velocity(self.pipette_dropping_speed, ID = 1)
            self.pipette_1_pos = 310
            self.dyna.write_pipette_ul(self.pipette_1_pos, ID = 1)
            self.com_state = 'send'
            
        elif self.dyna.pipette_is_in_position_ul(self.pipette_1_pos, ID = 1):
            self.sub_state = 'go to position'
            self.com_state = 'not send'
                
            
    elif self.sub_state == 'go to position':
        
        if self.com_state == 'not send':
            self.anycubic.move_axis_relative(x=self.target_pos[0]+self.offset_check[0], y=self.target_pos[1]+self.offset_check[1], z=self.pick_height + self.pick_offset, f=self.medium_speed)
            self.anycubic.finish_request()
            self.com_state = 'send'
            
        elif self.anycubic.get_finish_flag():
            self.sub_state = 'correction'
            self.com_state = 'not send'
            

    elif self.sub_state == 'correction':
        
        if self.com_state == 'not send':
            x, y, w, h = self.bbox
            target_px = [int(x+w/2), int(y+h/2)]
            self.target_pos = self.cam.cam_to_platform_space(target_px, (self.target_pos[0]+self.offset_check[0], self.target_pos[1]+self.offset_check[1], self.pick_height + self.pick_offset))
            
            if (self.target_pos[0]-self.petridish_pos[0])**2+(self.target_pos[1]-self.petridish_pos[1])**2 > self.petridish_radius**2:
                self.state = 'reset'
                self.sub_state = 'go to position'
                self.com_state = 'not send'         
                self.pick_attempt = 0    
            else:              
                self.anycubic.move_axis_relative(x=self.target_pos[0], y=self.target_pos[1], z=self.pick_height, f=self.slow_speed)
                # indirect move to go on top
                # self.anycubic.move_axis_relative(x=self.target_pos[0], y=self.target_pos[1], z=self.pick_height+2, f=self.slow_speed)
                # self.anycubic.move_axis_relative(z=self.pick_height, f=self.slow_speed)
                self.anycubic.finish_request()
                self.com_state = 'send'
        
        elif self.anycubic.get_finish_flag():
            self.sub_state = 'suck'
            self.com_state = 'not send'
    

    elif self.sub_state == 'suck':
        
        if self.com_state == 'not send':
            self.pipette_1_pos = self.pipette_1_pos - self.pipette_pumping_volume
            self.dyna.write_profile_velocity(self.pipette_pumping_speed, ID = 1)
            self.dyna.write_pipette_ul(self.pipette_1_pos, ID = 1)
            self.com_state = 'send'
            
        elif self.dyna.pipette_is_in_position_ul(self.pipette_1_pos, ID = 1):
            self.sub_state = 'check'
            self.com_state = 'not send'
            
    
    elif self.sub_state == 'check':
        
        if self.com_state == 'not send':
            self.anycubic.move_axis_relative(z=self.pick_height + self.pick_offset, f=self.slow_speed)
            self.anycubic.move_axis_relative(x=self.target_pos[0]+self.offset_check[0], y=self.target_pos[1]+self.offset_check[1], f=self.slow_speed)
            self.anycubic.finish_request()
            self.com_state = 'send'
            
        elif self.anycubic.get_finish_flag():
            
            # print(check_pickup(self))
            self.pick_attempt += 1
            
            if check_pickup(self):
                           
                release_tracker(self)
                self.state = 'picture'
                self.sub_state = 'go to position'
                self.com_state = 'not send' 
                self.pick_attempt = 0
                
            elif self.pipette_1_pos - self.pipette_pumping_volume >= 0 and self.pick_attempt < self.max_attempt:
                self.sub_state = 'correction'
                self.com_state = 'not send'
                
            else:
                release_tracker(self)
                self.state = 'reset'
                self.sub_state = 'go to position'
                self.com_state = 'not send'         
                self.pick_attempt = 0    

def picture(self):
    
    if self.sub_state == 'go to position':
        
        if self.com_state == 'not send':
            dest = destination(self)
            self.anycubic.move_axis_relative(z=self.safe_height, f=self.fast_speed)
            self.anycubic.move_axis_relative(x=self.picture_pos, y=dest[1], f=self.fast_speed)
            self.anycubic.finish_request()
            self.com_state = 'send'
            
        elif self.anycubic.get_finish_flag():
            
            # print(check_pickup_two(self))
            if delay(self, 0.5):
                if check_pickup_two(self):
                    self.state = 'place'
                    self.sub_state = 'go to position'
                    self.com_state = 'not send' 
                    
                else:
                    self.state = 'reset'
                    self.sub_state = 'go to position'
                    self.com_state = 'not send'            
                
def place(self):

    if self.sub_state == 'go to position':
        
        if self.com_state == 'not send':
            self.anycubic.move_axis_relative(z=self.safe_height, f=self.fast_speed)
            dest = destination(self)
            self.anycubic.move_axis_relative(x=dest[0], y=dest[1], f=self.fast_speed)
            self.anycubic.finish_request()
            self.com_state = 'send'
            
        elif self.anycubic.get_finish_flag():
            self.sub_state = 'go down'
            self.com_state = 'not send'       
                        
    
    elif self.sub_state == 'go down':
        
        if self.com_state == 'not send':
            self.anycubic.move_axis_relative(z=self.drop_height, f=self.fast_speed)
            self.anycubic.finish_request()
            self.com_state = 'send'
            
        elif self.anycubic.get_finish_flag():
            self.sub_state = 'blow'
            self.com_state = 'not send'   
            
            
            
    elif self.sub_state == 'blow':
        
        if self.com_state == 'not send':
            self.dyna.write_profile_velocity(self.pipette_dropping_speed, ID = 1)
            self.pipette_1_pos = self.pipette_1_pos + self.pipette_dropping_volume
            self.dyna.write_pipette_ul(self.pipette_1_pos, ID = 1)
            self.com_state = 'send'
            
        elif self.dyna.pipette_is_in_position_ul(self.pipette_1_pos, ID = 1):
            self.sub_state = 'go up'
            self.com_state = 'not send'     


    elif self.sub_state == 'go up':
        
        if self.com_state == 'not send':
            self.anycubic.move_axis_relative(z=self.safe_height, f=self.fast_speed)
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
            self.anycubic.move_axis_relative(z=self.safe_height, f=self.fast_speed)
            self.anycubic.move_axis_relative(x=self.picture_pos, y=dest[1], f=self.fast_speed)
            self.anycubic.finish_request()
            self.com_state = 'send'
            
        elif self.anycubic.get_finish_flag():
            
            # print(check_pickup_two(self))
            if delay(self, 0.5):
                if check_pickup_two(self):
                    self.state = 'place'
                    self.sub_state = 'go to position'
                    self.com_state = 'not send' 
                    
                else:
                    self.nb_sample += 1
                    self.state = 'reset'
                    self.sub_state = 'go to position'
                    self.com_state = 'not send'            
              
def reset(self):
    
    if self.sub_state == 'go to position':
        
        if self.com_state == 'not send':
            release_tracker(self)
            self.anycubic.move_axis_relative(z=self.safe_height, f=self.fast_speed)
            self.anycubic.move_axis_relative(x=self.reset_pos[0], y=self.reset_pos[1], f=self.fast_speed)
            self.anycubic.move_axis_relative(z=self.reset_pos[2], f=self.fast_speed) 
            self.anycubic.finish_request() 
            self.com_state = 'send'  
            
        elif self.anycubic.get_finish_flag():
            self.sub_state = 'empty pipette'
            self.com_state = 'not send'
            
            
    elif self.sub_state == 'empty pipette':
        
        if self.com_state == 'not send':
            self.dyna.write_profile_velocity(self.pipette_dropping_speed, ID = 1)
            self.pipette_1_pos = self.pipette_empty
            self.dyna.write_pipette_ul(self.pipette_1_pos, ID = 1)
            self.com_state = 'send'
            
        elif self.dyna.pipette_is_in_position_ul(self.pipette_1_pos, ID = 1):
            if self.nb_sample == self.nb_sample_well:
                self.well_num += 1
                self.nb_sample = 0
                
                if self.well_num == len(self.culture_well) or self.well_num == self.number_of_well:
                    self.state = 'Done'
                else:
                    if self.well_preparation:
                        self.state = 'preparing gel'
                    else:
                        self.state = 'detect'
                    self.sub_state = 'go to position'
                    self.com_state = 'not send'   
            else:
                self.state = 'detect'
                self.sub_state = 'go to position'
                self.com_state = 'not send'   
            
def gui_parameter(self, direction=None):
    
    if direction == 'up':
        
        if self.gui_menu == 0:
            self.pick_height += 0.1
        if self.gui_menu == 1:
            self.drop_height += 0.1
        if self.gui_menu == 2:
            self.slow_speed += 50
        if self.gui_menu == 3:
            self.medium_speed += 50
        if self.gui_menu == 4:
            self.fast_speed += 50     
        if self.gui_menu == 5:
            self.pipette_pumping_volume += 1
        if self.gui_menu == 6:
            self.pipette_pumping_speed += 1
        if self.gui_menu == 7:
            self.pipette_dropping_volume += 1
        if self.gui_menu == 8:
            self.pipette_dropping_speed += 1
            
        if self.gui_menu == 9:
            self.solution_pumping_height += 0.1
        if self.gui_menu == 10:
            self.solution_A_pumping_speed += 1
        if self.gui_menu == 11:
            self.solution_A_dropping_speed += 1
        if self.gui_menu == 12:
            self.solution_A_pumping_volume += 1
        if self.gui_menu == 13:
            self.solution_B_pumping_speed += 1
        if self.gui_menu == 14:
            self.solution_B_dropping_speed += 1
        if self.gui_menu == 15:
            self.solution_B_pumping_volume += 1
        if self.gui_menu == 16:
            self.num_mix  += 1
        if self.gui_menu == 17:
            self.num_wash += 1
        if self.gui_menu == 18:
            self.max_attempt += 1
        if self.gui_menu == 19:
            self.well_preparation = True
        if self.gui_menu == 20:
            if self.nb_sample_well < 8:
                self.nb_sample_well += 1
        if self.gui_menu == 21:
            if self.number_of_well < 6:
                self.number_of_well += 1
    
    if direction == 'down':
        
        if self.gui_menu == 0:
            self.pick_height -= 0.1
        if self.gui_menu == 1:
            self.drop_height -= 0.1
        if self.gui_menu == 2:
            self.slow_speed -= 50
        if self.gui_menu == 3:
            self.medium_speed -= 50
        if self.gui_menu == 4:
            self.fast_speed -= 50     
        if self.gui_menu == 5:
            self.pipette_pumping_volume -= 1
        if self.gui_menu == 6:
            self.pipette_pumping_speed -= 1
        if self.gui_menu == 7:
            self.pipette_dropping_volume -= 1
        if self.gui_menu == 8:
            self.pipette_dropping_speed -= 1
            
        if self.gui_menu == 9:
            self.solution_pumping_height -= 0.1
        if self.gui_menu == 10:
            self.solution_A_pumping_speed -= 1
        if self.gui_menu == 11:
            self.solution_A_dropping_speed -= 1
        if self.gui_menu == 12:
            self.solution_A_pumping_volume -= 1
        if self.gui_menu == 13:
            self.solution_B_pumping_speed -= 1
        if self.gui_menu == 14:
            self.solution_B_dropping_speed -= 1
        if self.gui_menu == 15:
            self.solution_B_pumping_volume -= 1
        if self.gui_menu == 16:
            self.num_mix  -= 1
        if self.gui_menu == 17:
            self.num_wash -= 1
        if self.gui_menu == 18:
            self.max_attempt -= 1
        if self.gui_menu == 19:
            self.well_preparation = False
        if self.gui_menu == 20:
            if self.nb_sample_well > 1:
                self.nb_sample_well -= 1
        if self.gui_menu == 21:
            if self.number_of_well > 1:
                self.number_of_well -= 1
            
    if direction is None:
        
        if self.gui_menu == 0:
            return self.pick_height
        if self.gui_menu == 1:
            return self.drop_height
        if self.gui_menu == 2:
            return self.slow_speed
        if self.gui_menu == 3:
            return self.medium_speed
        if self.gui_menu == 4:
            return self.fast_speed       
        if self.gui_menu == 5:
            return self.pipette_pumping_volume
        if self.gui_menu == 6:
            return self.pipette_pumping_speed
        if self.gui_menu == 7:
            return self.pipette_dropping_volume
        if self.gui_menu == 8:
            return self.pipette_dropping_speed
        
        if self.gui_menu == 9:
            return self.solution_pumping_height
        if self.gui_menu == 10:
            return self.solution_A_pumping_speed
        if self.gui_menu == 11:
            return self.solution_A_dropping_speed
        if self.gui_menu == 12:
            return self.solution_A_pumping_volume
        if self.gui_menu == 13:
            return self.solution_B_pumping_speed
        if self.gui_menu == 14:
            return self.solution_B_dropping_speed
        if self.gui_menu == 15:
            return self.solution_B_pumping_volume
        if self.gui_menu == 16:
            return self.num_mix
        if self.gui_menu == 17:
            return self.num_wash
        if self.gui_menu == 18:
            return self.max_attempt       
        if self.gui_menu == 19:
            if self.well_preparation:
                return 'yes'
            else:
                return 'no'
        if self.gui_menu == 20:
            return self.nb_sample_well
        if self.gui_menu == 21:
            return self.number_of_well


        
    
def display(self, position):
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    color = (255, 255, 255) #BGR
    thickness = 2

    fontScale = 0.8 
    
    name, unit = self.gui_menu_label[(self.gui_menu)%len(self.gui_menu_label), 0], self.gui_menu_label[(self.gui_menu)%len(self.gui_menu_label), 1]
    self.imshow = cv2.putText(self.imshow, name, position, font, 
                            fontScale, color, thickness, cv2.LINE_AA)  
    
    pos = position
    pos[0] = pos[0] + 363 
    if self.gui_menu == 19:
        val = gui_parameter(self)
    else:
        val = str(round(gui_parameter(self), 2))
        
    self.imshow = cv2.putText(self.imshow, val, position, font, 
                            fontScale, color, thickness, cv2.LINE_AA)    
    
    size, _ = cv2.getTextSize(val, font, fontScale, thickness)
    pos[0] = pos[0] + size[0] + 8
    self.imshow = cv2.putText(self.imshow, unit, position, font, 
                            fontScale, color, thickness, cv2.LINE_AA)  

def save_parameters(self):
    
    params = []
    params.append(self.fast_speed)
    params.append(self.medium_speed)
    params.append(self.slow_speed)
    params.append(self.drop_height)
    params.append(self.pipette_dropping_speed)
    params.append(self.pipette_dropping_volume)
    params.append(self.pick_height)
    params.append(self.pipette_pumping_speed)
    params.append(self.pipette_pumping_volume)
    params.append(self.solution_pumping_height)
    params.append(self.solution_A_pumping_speed)
    params.append(self.solution_A_dropping_speed)
    params.append(self.solution_A_pumping_volume)
    params.append(self.solution_B_pumping_speed)
    params.append(self.solution_B_dropping_speed)
    params.append(self.solution_B_pumping_volume)
    params.append(self.num_mix)
    params.append(self.num_wash)
    params.append(self.offset)
    params.append(self.max_attempt)
    params.append(self.well_preparation)
    params.append(self.nb_sample_well)
    params.append(self.number_of_well)
                
    pickle.dump(params, open('Platform/Calibration/parameters.pkl', 'wb'))
    
def load_parameters(self):

    params = pickle.load(open('Platform/Calibration/parameters.pkl', 'rb'))
    
    self.fast_speed = params[0]
    self.medium_speed = params[1]
    self.slow_speed = params[2]
    self.drop_height = params[3]
    self.pipette_dropping_speed = params[4]
    self.pipette_dropping_volume = params[5]
    self.pick_height = params[6]
    self.pipette_pumping_speed = params[7]
    self.pipette_pumping_volume = params[8]
    self.solution_pumping_height = params[9]
    self.solution_A_pumping_speed = params[10]
    self.solution_A_dropping_speed = params[11]
    self.solution_A_pumping_volume = params[12]
    self.solution_B_pumping_speed = params[13]
    self.solution_B_dropping_speed = params[14]
    self.solution_B_pumping_volume = params[15]
    self.num_mix = params[16]
    self.num_wash = params[17]
    self.offset = params[18]
    self.max_attempt = params[19]
    self.well_preparation = params[20]
    self.nb_sample_well = params[21]
    self.number_of_well = params[22]


goodbye ="""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡤⠴⠒⠤⣄⡀⠀⠀⠀⠀⢠⣾⠉⠉⠉⠉⠑⠒⠦⢄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⠋⠀⠀⠀⠀⠀⠉⠲⡄⠀⢠⠏⡏⠀⠀⠀⠀⠀⠀⠀⠀⠉⠳⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⢤⣤⣀⡀⠀⠀⠀⠀⠀⢰⡏⠀⠀⠀⠀⠀⠀⠀⠀⠘⢆⢸⠀⡇⠀⠀⠀⢀⣀⠀⠀⠀⠀⠀⢸⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⠏⠀⠀⠀⠀⠈⠙⠢⣄⠀⠀⣿⠀⠀⠀⢰⣿⣷⣆⠀⠀⠀⠘⣾⠀⠇⠀⠀⠀⢾⣿⣿⣦⠀⠀⠀⠀⢻⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⣀⡤⣄⠀⠀⠀⣼⡇⠀⠀⠀⢀⣀⠀⠀⠀⠈⠳⣴⢿⡄⠀⠀⢸⡿⣿⢹⠀⠀⠀⠀⣿⠀⡆⠀⠀⠀⣼⠻⣇⣸⠀⠀⠀⠀⣸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢀⡴⠚⠉⠀⠀⠈⠳⡄⠀⣿⡇⠀⠀⠀⣿⣿⡷⡄⠀⠀⠀⢹⣆⢧⠀⠀⠀⠙⠿⠋⠀⠀⠀⠀⣿⠀⡇⠀⠀⠀⠙⠛⠉⠁⠀⠀⠀⢠⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢠⠟⠀⠀⠀⠀⢀⣤⣾⣷⣀⡇⢣⠀⠀⠀⢻⣟⣄⣷⠀⠀⠀⠈⣿⣾⣆⠀⠀⠀⠀⠀⠀⠀⠀⣸⢿⢰⡁⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡾⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣠⡏⠀⠀⠀⣼⡟⣿⣿⡿⠛⠉⢻⣞⣧⠀⠀⠀⠉⠛⠁⠀⠀⠀⠀⡿⣿⣿⣦⣀⠀⠀⠀⠀⣠⣾⡏⢸⣠⣧⣤⣄⣤⣤⣤⣤⣤⣴⣾⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⠀⠀⠀⢸⠋⣿⠛⠁⠀⠀⠀⠀⠻⣯⣷⣄⠀⠀⠀⠀⠀⠀⢀⣼⠁⠘⠿⣿⣿⣻⣿⣿⣿⣿⠏⠀⣾⣿⣿⣿⣿⣿⣿⣿⡿⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⡟⣇⠀⠀⠈⢿⣏⢧⣴⣶⡆⠀⠀⠀⢿⣿⣿⢳⢦⣤⣤⣤⣶⣿⠟⠀⠀⠀⠀⠉⠉⠛⠋⢩⡤⠖⠒⠛⠛⡿⢁⣾⠋⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⣷⠀⠀⠀⠀⢀⣤⠤⠤⣀⡀⠀
⣇⠘⣆⠀⠀⠀⠙⠻⠿⠛⠃⠀⠀⠀⣸⡙⠻⢿⣿⣿⣿⣿⠿⠋⠀⣀⡤⠤⠒⠚⠳⣄⢠⣿⠁⠀⠀⠀⢠⠇⡏⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⠀⠀⢀⡴⢫⡇⠀⠀⠀⠈⠙
⠘⣶⣿⣷⣄⡀⠀⠀⠀⠀⠀⠀⣀⣼⣿⠇⠀⠀⠀⣀⣀⣀⠀⢀⣼⣿⣦⡀⠀⠀⠀⠈⢻⡏⠀⠀⠀⠀⡞⠀⡇⢸⠀⠀⠀⠀⢰⣾⣶⣶⣶⣶⣶⡏⠀⠀⡼⠀⡞⠀⠀⠀⠀⠀⢸
⠀⠈⠻⣿⣿⣿⣶⢶⡶⡶⣶⣾⣿⡿⠋⣠⠴⠚⠉⠁⠀⠉⠙⠺⡿⢿⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⣸⠃⢰⠀⢸⠀⠀⠀⠀⠘⠛⠛⠿⠿⢿⡏⠀⠀⢰⠃⢠⠇⠀⠀⠀⠀⠀⠌
⠀⠀⠀⠈⠙⠻⠿⠼⠽⠿⠿⠟⠋⢰⡟⠁⠀⠀⢀⣤⣄⡀⠀⠀⠹⡆⠙⢿⣿⣿⣦⡀⠀⠀⠀⠀⢰⡇⠀⢸⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⡞⠀⡜⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡾⢳⡀⠀⠀⠈⢿⡿⠇⠀⠀⣼⠃⠀⠀⠙⢿⣿⣿⣷⠀⠀⠀⠈⡇⠀⢸⠀⡄⠀⠀⠀⠀⢰⣶⣤⣤⣤⣼⠃⠀⢰⠃⢰⠃⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢷⠀⢣⠀⠀⠀⠀⠀⠀⠀⠈⠋⠉⠲⣄⠀⠀⠙⢿⠸⡄⠀⠀⠀⢳⠀⢸⠀⡇⠀⠀⠀⠀⠸⣿⣿⣿⣿⣃⠀⠀⣞⣠⣾⣤⣀⣀⠀⠀⡄⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣆⠈⣇⠀⠀⠀⠀⣠⣤⣀⠀⠀⠀⠘⣆⠀⠀⠸⡄⢳⠀⠀⠀⠸⡆⢸⠀⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠘⠻⢿⣿⣿⣿⣿⡿⠞⠁⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⡆⠘⡄⠀⠀⠀⢻⣿⣿⠆⠀⠀⠀⢸⠀⠀⠀⣇⠘⡆⠀⢀⣀⣧⢸⢀⣿⣶⣤⣤⣤⣀⣀⣀⠀⢀⡏⠀⢀⣴⠟⠁⠀⠀⠈⢳⡀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⡄⠹⡄⠀⠀⠈⠉⠁⠀⠀⠀⣠⡾⠀⠀⠀⢹⢀⣿⣿⣿⡿⠃⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⢰⣯⡏⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢳⠀⠹⡄⠀⠀⠀⢀⣠⣴⣾⣿⠃⠀⠀⠀⠘⠿⠟⠛⠛⠁⠀⠀⠀⠉⠉⠉⠛⠛⠛⠿⠟⠁⠀⠀⢾⣿⣷⣄⡀⠀⠀⢀⡼⠃⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢧⠀⢳⣴⣶⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢿⣿⣿⣿⣿⡿⠟⠁⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣦⣿⣿⡿⠟⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀   ⠀⠀⠀⠀⠈⠉⠉⣀⠀⠀⠀⠀⠀⠀⠀
"""