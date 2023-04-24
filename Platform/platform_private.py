import computer_vision as cv
import cv2
import math
import time


class sample:
    
    def __init__(self, num, x, y, image = None):
        self.num = num
        self.x = x
        self.y = y
        self.image = None


# Private methodes
            
def destination(self):
    
    # mod = int(self.nb_sample/self.nb_pos[1])
    # 
    # print('Tube n° ', self.number_sample)
    # print('x offset', mod)
    # print('y offset', self.number_sample%self.num_y)
    # 
    # return round(self.dropping_pos[0]-self.offset_pos*mod, 2), round(self.dropping_pos[1]-self.offset_pos*(self.nb_sample%self.nb_pos[1]), 2)
    
    angle = math.pi/180.0*30*(self.nb_sample)
    radius = 15

    return [self.dropping_pos[0]+radius*math.cos(angle), self.dropping_pos[1]+radius*math.sin(angle)]


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
            self.anycubic.move_axis(z=self.safe_height, f=self.fast_speed)
            self.anycubic.move_axis(x=self.detection_place[0], y=self.detection_place[1], z=self.detection_place[2], f=self.fast_speed)
            self.anycubic.finish_request()
            self.com_state = 'send'
            
        elif self.anycubic.get_finish_flag():
            self.sub_state = 'analyse picture'
            self.com_state = 'not send'
            
            
    elif self.sub_state == 'analyse picture':
          
        target_px, optimal_angle = cv.detection(self)
                
        if target_px is not None:
             
            set_tracker(self, target_px)
            self.target_pos = self.cam.cam_to_platform_space(target_px, self.detection_place)
            self.offset_check = (self.dist_check*math.sin(optimal_angle), self.dist_check*math.cos(optimal_angle))

            self.state = 'temp1'
            self.sub_state = 'empty pipette'
            self.com_state = 'not send'
            self.detect_attempt = 0
        else:
            self.detect_attempt += 1
            
            if self.detect_attempt == self.max_attempt:
                self.state = 'pause'
                self.last_state = 'detect'
                self.detect_attempt = 0
                print('No tissue detected')
    
    
def pick(self):
            
    
    if self.sub_state == 'empty pipette':
    
        if self.com_state == 'not send':
            self.dyna.write_profile_velocity(self.pipette_dropping_speed, ID = 1)
            self.pipette_pos = 50
            # self.dyna.write_position(self.dyna.pipette(self.pipette_pos), ID = 1)
            self.dyna.write_pipette(self.pipette_pos, ID = 1)
            self.com_state = 'send'
            
        elif self.dyna.pipette_is_in_position(self.pipette_pos, ID = 1):
            self.sub_state = 'go to position'
            self.com_state = 'not send'
                
            
    elif self.sub_state == 'go to position':
        
        if self.com_state == 'not send':
            self.anycubic.move_axis(x=self.target_pos[0], y=self.target_pos[1], z=self.pick_height + self.pick_offset, f=self.slow_speed)
            self.anycubic.finish_request()
            self.com_state = 'send'
            
        elif self.anycubic.get_finish_flag():
            self.sub_state = 'correction'
            self.com_state = 'not send'
            

    elif self.sub_state == 'correction':
        
        if self.com_state == 'not send':
            x, y, w, h = self.bbox
            target_px = [int(x+w/2), int(y+h/2)]
            self.target_pos = self.cam.cam_to_platform_space(target_px, (self.target_pos[0], self.target_pos[1], self.pick_height + self.pick_offset))
            self.anycubic.move_axis(x=self.target_pos[0], y=self.target_pos[1], z=self.pick_height, f=self.slow_speed)
            self.anycubic.finish_request()
            self.com_state = 'send'
        
        elif self.anycubic.get_finish_flag():
            self.sub_state = 'suck'
            self.com_state = 'not send'
    

    elif self.sub_state == 'suck':
        
        if self.com_state == 'not send':
            self.pipette_pos = self.pipette_pos - self.pipette_pumping_volume
            self.dyna.write_profile_velocity(self.pipette_pumping_speed, ID = 1)
            # self.dyna.write_position(self.dyna.pipette(self.pipette_pos), ID = 1)
            self.dyna.write_pipette(self.pipette_pos, ID = 1)
            self.com_state = 'send'
            
        elif self.dyna.pipette_is_in_position(self.pipette_pos, ID = 1):
            self.sub_state = 'check'
            self.com_state = 'not send'
            
    
    elif self.sub_state == 'check':
        
        if self.com_state == 'not send':
            self.anycubic.move_axis(z=self.pick_height + self.pick_offset, f=self.slow_speed)
            self.anycubic.move_axis(x=self.target_pos[0]+self.offset_check[0], y=self.target_pos[1]+self.offset_check[1], f=self.slow_speed)
            self.anycubic.finish_request()
            self.com_state = 'send'
            
        elif self.anycubic.get_finish_flag():
            
            print(check_pickup(self))
            
            if check_pickup(self):
                           
                release_tracker(self)
                self.state = 'place'
                self.sub_state = 'go to position'
                self.com_state = 'not send' 
                
            elif self.pipette_pos - self.pipette_pumping_volume >= 0:
                self.sub_state = 'go to position'
                self.com_state = 'not send'
            else:
                release_tracker(self)
                self.state = 'reset'
                self.sub_state = 'go to position'
                self.com_state = 'not send'       
            

def place(self):

    if self.sub_state == 'go to position':
        
        if self.com_state == 'not send':
            self.anycubic.move_axis(z=self.safe_height, f=self.medium_speed)
            dest = destination(self)
            self.anycubic.move_axis(x=dest[0], y=dest[1], f=self.medium_speed)
            self.anycubic.finish_request()
            self.com_state = 'send'
            
        elif self.anycubic.get_finish_flag():
            self.sub_state = 'go down'
            self.com_state = 'not send'       
                        
    
    elif self.sub_state == 'go down':
        
        if self.com_state == 'not send':
            self.anycubic.move_axis(z=self.drop_height, f=self.slow_speed)
            self.anycubic.finish_request()
            self.com_state = 'send'
            
        elif self.anycubic.get_finish_flag():
            self.sub_state = 'blow'
            self.com_state = 'not send'   
            
            
            
    elif self.sub_state == 'blow':
        
        if self.com_state == 'not send':
            self.dyna.write_profile_velocity(self.pipette_dropping_speed, ID = 1)
            self.pipette_pos = self.pipette_pos + self.pipette_dropping_volume
            # self.dyna.write_position(self.dyna.pipette(self.pipette_pos), ID = 1)
            self.dyna.write_pipette(self.pipette_pos, ID = 1)
            self.com_state = 'send'
            
        elif self.dyna.pipette_is_in_position(self.pipette_pos, ID = 1):
            self.nb_sample += 1
            self.sub_state = 'go up'
            self.com_state = 'not send'     


    elif self.sub_state == 'go up':
        
        if self.com_state == 'not send':
            self.anycubic.move_axis(z=self.safe_height, f=self.fast_speed)
            self.anycubic.finish_request()
            self.com_state = 'send'
        
        elif self.anycubic.get_finish_flag():
            self.state = 'reset'
            self.sub_state = 'go to position'
            self.com_state = 'not send'
            

def reset(self):

    if self.sub_state == 'go to position':
        
        if self.com_state == 'not send':
            release_tracker(self=self)
            self.anycubic.move_axis(z=self.safe_height, f=self.fast_speed)
            self.anycubic.move_axis(x=self.reset_pos[0], y=self.reset_pos[1], f=self.fast_speed)
            self.anycubic.move_axis(z=self.reset_pos[2], f=self.fast_speed) 
            self.anycubic.finish_request() 
            self.com_state = 'send'  
            
        elif self.anycubic.get_finish_flag():
            self.sub_state = 'empty pipette'
            self.com_state = 'not send'
            
            
    elif self.sub_state == 'empty pipette':
        
        if self.com_state == 'not send':
            self.dyna.write_profile_velocity(self.pipette_dropping_speed, ID = 1)
            self.pipette_pos = self.pipette_empty
            # self.dyna.write_position(self.dyna.pipette(self.pipette_pos), ID = 1)
            self.dyna.write_pipette(self.pipette_pos, ID = 1)
            self.com_state = 'send'
            
        elif self.dyna.pipette_is_in_position(self.pipette_pos, ID = 1):
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
            self.slow_speed += 1
        if self.gui_menu == 3:
            self.medium_speed += 1
        if self.gui_menu == 4:
            self.fast_speed += 1        
        if self.gui_menu == 5:
            self.pipette_pumping_volume += 1
        if self.gui_menu == 6:
            self.pipette_pumping_speed += 1
        if self.gui_menu == 7:
            self.pipette_dropping_volume += 1
        if self.gui_menu == 8:
            self.pipette_dropping_speed += 1 
    
    if direction == 'down':
        
        if self.gui_menu == 0:
            self.pick_height -= 0.1
        if self.gui_menu == 1:
            self.drop_height -= 0.1
        if self.gui_menu == 2:
            self.slow_speed -= 1
        if self.gui_menu == 3:
            self.medium_speed -= 1
        if self.gui_menu == 4:
            self.fast_speed -= 1        
        if self.gui_menu == 5:
            self.pipette_pumping_volume -= 1
        if self.gui_menu == 6:
            self.pipette_pumping_speed -= 1
        if self.gui_menu == 7:
            self.pipette_dropping_volume -= 1
        if self.gui_menu == 8:
            self.pipette_dropping_speed -= 1 
            
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
        
        
def display(self, position):
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    color = (255, 255, 255) #BGR
    thickness = 2

    fontScale = 0.8 
    
    text = self.gui_menu_label[(self.gui_menu)%len(self.gui_menu_label)]
    self.imshow = cv2.putText(self.imshow, text, position, font, 
                            fontScale, color, thickness, cv2.LINE_AA)  
    
    pos = position
    pos[0] = pos[0] + 250 
    text = str(round(gui_parameter(self), 2))
    self.imshow = cv2.putText(self.imshow, text, position, font, 
                            fontScale, color, thickness, cv2.LINE_AA)  
    

def temp1(self):
    
    if self.sub_state == 'empty pipette':
        
        if self.com_state == 'not send':
            self.dyna.write_profile_velocity(self.pipette_dropping_speed, ID = 1)
            self.pipette_pos = 50
            # self.dyna.write_position(self.dyna.pipette(self.pipette_pos), ID = 1)
            self.dyna.write_pipette(self.pipette_pos, ID = 1)
            self.com_state = 'send'
            
        elif self.dyna.pipette_is_in_position(self.pipette_pos, ID = 1):
            self.sub_state = 'go to position'
            self.com_state = 'not send'
                
            
    elif self.sub_state == 'go to position':
        
        if self.com_state == 'not send':
            self.anycubic.move_axis(x=self.target_pos[0]+self.dist_check, y=self.target_pos[1], z=self.pick_height + self.pick_offset, f=self.slow_speed)
            self.anycubic.finish_request()
            self.com_state = 'send'
            
        elif self.anycubic.get_finish_flag():
            self.save = 0
            self.sub_state = 'save'
            self.com_state = 'not send'
            
    elif self.sub_state == 'save':
            
        if self.com_state == 'not send':
            cv2.imwrite(r"C:\Users\APrap\Documents\CREATE\Pick-and-Place\Pictures\detection\image_check" + str(self.counter) + ".png", self.frame)
            self.counter += 1
            self.save += 1
            if self.save >= 5:
                self.com_state = 'send'
            
        else:
            self.sub_state = 'correction'
            self.com_state = 'not send'       

    elif self.sub_state == 'correction':
        
        if self.com_state == 'not send':
            x, y, w, h = self.bbox
            target_px = [int(x+w/2), int(y+h/2)]
            self.target_pos = self.cam.cam_to_platform_space(target_px, (self.target_pos[0]+self.dist_check, self.target_pos[1], self.pick_height + self.pick_offset))
            self.anycubic.move_axis(x=self.target_pos[0], y=self.target_pos[1], z=self.pick_height, f=self.slow_speed)
            self.anycubic.finish_request()
            self.com_state = 'send'
        
        elif self.anycubic.get_finish_flag():
            self.sub_state = 'suck'
            self.com_state = 'not send'
    

    elif self.sub_state == 'suck':
        
        if self.com_state == 'not send':
            self.pipette_pos = self.pipette_pos - self.pipette_pumping_volume
            self.dyna.write_profile_velocity(self.pipette_pumping_speed, ID = 1)
            # self.dyna.write_position(self.dyna.pipette(self.pipette_pos), ID = 1)
            self.dyna.write_pipette(self.pipette_pos, ID = 1)
            self.com_state = 'send'
            
        elif self.dyna.pipette_is_in_position(self.pipette_pos, ID = 1):
            self.sub_state = 'check'
            self.com_state = 'not send'
            
    
    elif self.sub_state == 'check':
        
        if self.com_state == 'not send':
            self.anycubic.move_axis(z=self.pick_height + self.pick_offset, f=self.slow_speed)
            self.anycubic.move_axis(x=self.target_pos[0]+self.dist_check, y=self.target_pos[1], f=self.slow_speed)
            self.anycubic.finish_request()
            self.com_state = 'send'
            
        elif self.anycubic.get_finish_flag():
            
            print(check_pickup(self))
            
            if check_pickup(self):
                           
                release_tracker(self)
                self.state = 'place'
                self.sub_state = 'go to position'
                self.com_state = 'not send' 
                
            elif self.pipette_pos - self.pipette_pumping_volume >= 0:
                self.sub_state = 'go to position'
                self.com_state = 'not send'
            else:
                release_tracker(self)
                self.state = 'reset'
                self.sub_state = 'go to position'
                self.com_state = 'not send'       
