import computer_vision as cv
import cv2


class sample:
    
    def __init__(self, num, x, y, image = None):
        self.num = num
        self.x = x
        self.y = y
        self.image = None


# Private methodes
            
def destination(self):
    
    mod = int(self.nb_sample/self.nb_pos[1])
    
    # print('Tube n° ', self.number_sample)
    # print('x offset', mod)
    # print('y offset', self.number_sample%self.num_y)
    
    return round(self.dropping_pos[0]-self.offset_pos*mod, 2), round(self.dropping_pos[1]-self.offset_pos*(self.nb_sample%self.nb_pos[1]), 2)


def set_tracker(self, target_rel):

    bbox = [int(target_rel[1]-self.roi_size/2),int(target_rel[0]-self.roi_size/2), self.roi_size, self.roi_size]
    self.tracker.init(self.frame, bbox)
    self.track_on = True
    

def release_tracker(self):
    
    self.track_on = False
    self.success = False
    self.tracker = cv2.TrackerMIL.create() 
    
    
def check_pickup(self):
    
    x, y, w, h = [int(i) for i in self.bbox]
    tracker_pos = [int(x+w/2), int(y+h/2)]
    
    if tracker_pos[1] > 440:
        return True
    else:
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
        
        target, target_rel =  cv.detect(self.frame, self.detection_place, self.detector, self.mask)
        
        if target is not None:
            self.sample_list.append(sample(self.nb_sample, target[0], target[1]))
            self.nb_sample += 1
             
            set_tracker(self, target_rel)
        
            self.state = 'pick'
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
            self.dyna.write_profile_velocity(self.pipette_empty_speed, ID = 1)
            self.dyna.write_position(self.dyna.pipette(80), ID = 1)
            self.com_state = 'send'
            
        elif self.dyna.pipette_is_in_position(80, ID = 1):
            self.sub_state = 'go to position'
            self.com_state = 'not send'
                
            
    elif self.sub_state == 'go to position':
        
        if self.com_state == 'not send':
            self.anycubic.move_axis(x=self.sample_list[self.nb_sample-1].x, y=self.sample_list[self.nb_sample-1].y, z=self.pick_height + self.pick_offset, f=self.slow_speed)
            self.anycubic.move_axis(z=self.pick_height, f=self.slow_speed)
            self.anycubic.finish_request()
            self.com_state = 'send'
            
        elif self.anycubic.get_finish_flag():
            self.sub_state = 'suck'
            self.com_state = 'not send'
            

    elif self.sub_state == 'suck':
        
        if self.com_state == 'not send':
            self.dyna.write_profile_velocity(self.pipette_fill_speed, ID = 1)
            self.dyna.write_position(self.dyna.pipette(50), ID = 1)
            self.com_state = 'send'
            
        elif self.dyna.pipette_is_in_position(50, ID = 1):
            self.sub_state = 'check'
            self.com_state = 'not send'
            
    
    elif self.sub_state == 'check':
        
        if self.com_state == 'not send':
            self.anycubic.move_axis(z=self.pick_height + self.pick_offset, f=self.slow_speed)
            self.anycubic.move_axis(x=self.sample_list[self.nb_sample-1].x+10, f=self.slow_speed)
            self.anycubic.finish_request()
            self.com_state = 'send'
            
        elif self.anycubic.get_finish_flag():
            
            print('Pickup : ', check_pickup(self))
            
            release_tracker(self)
            self.state = 'reset'
            self.sub_state = 'go to position'
            self.com_state = 'not send' 
            
            # if cv.check_pickup(self.frame, self.detector):
            #     self.state = 'place'
            #     self.sub_state = 'go to position'
            #     self.com_state = 'not send'    
            # else:
            #     self.state = 'reset'
            #     self.sub_state = 'go to position'
            #     self.com_state = 'not send'
                
            

def place(self):

    if self.sub_state == 'go to position':
        
        if self.com_state == 'not send':
            self.anycubic.move_axis(z=self.safe_height, f=self.medium_speed)
            dest_x, dest_y = destination(self)
            self.anycubic.move_axis(x=dest_x, y=dest_y, f=self.medium_speed)
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
            self.dyna.write_profile_velocity(self.pipette_empty_speed, ID = 1)
            self.dyna.write_position(self.dyna.pipette(60), ID = 1)
            self.com_state = 'send'
            
        elif self.dyna.pipette_is_in_position(60, ID = 1):
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
            self.dyna.write_profile_velocity(self.pipette_empty_speed, ID = 1)
            self.dyna.write_position(self.dyna.pipette(100), ID = 1)
            self.com_state = 'send'
            
        elif self.dyna.pipette_is_in_position(100, ID = 1):
            self.dyna.write_position(self.dyna.pipette(0), ID = 1)
            self.state = 'detect'
            self.sub_state = 'go to position'
            self.com_state = 'not send'   