from Platform.parameters import*
import Platform.computer_vision as cv
from time import sleep
        
    
def reset(self):
    
    # Go to position
    
    self.anycubic.move_axis(z=self.safe_height, f=self.fast_speed)
    self.anycubic.move_axis(x=self.reset_pos[0], y=self.reset_pos[1], f=self.fast_speed)
    self.anycubic.move_axis(z=self.reset_pos[2], f=self.fast_speed) 
    self.anycubic.finish_request() 
    
    while not self.anycubic.get_finish_flag():
        if self.state is not RESET:
            return
        
    # Empty pipette
    print('empty')
    self.dyna.write_profile_velocity(self.pipette_empty_speed, ID = 1)
    self.dyna.write_position(self.dyna.pipette(100), ID = 1)
    print('wait')
    sleep(1) # Attente dynamique !!!!!!!!!!!!!!!!!!!!!!!!!!!
    
    self.dyna.write_profile_velocity(self.pipette_empty_speed, ID = 1)
    self.dyna.write_position(self.dyna.pipette(0), ID = 1)
    
    # Detect
    
    self.state = DETECT


def detect(self):
        
    # Go to detection place
    
    self.anycubic.move_axis(z=self.safe_height, f=self.fast_speed)
    self.anycubic.move_axis(x=self.detection_place[0], y=self.detection_place[1], z=self.detection_place[2], f=self.fast_speed)
    self.anycubic.finish_request()
    
    while not self.anycubic.get_finish_flag():
        if self.state is not DETECT:
            return
        
    # Analyse picutre
    
    target = None
    
    while target is None:
                
        target =  cv.detect(self.frame, self.detection_place, self.detector, self.mask)
        
        if self.detect_attempt == self.max_attempt:
            self.state = PAUSE
            print('No tissue detected, waiting...')
            return

        self.detect_attempt += 1
                
    self.detect_attempt = 0
    
    self.sample_list.append(Sample(self.nb_sample, target[0], target[1]))
    self.nb_sample += 1
    
    # Pick
    
    self.state = PICK
    
        
def pick(self):
            
    # Empty pipette
    
    self.dyna.write_profile_velocity(self.pipette_empty_speed, ID = 1)
    self.dyna.write_position(self.dyna.pipette(80), ID = 1)
    
    while not self.dyna.pipette_is_in_position(80, ID = 1):
        if self.state is not PICK:
            return
        
    # Go to position
    
    self.anycubic.move_axis(x=self.sample_list[self.nb_sample-1].x, y=self.sample_list[self.nb_sample-1].y, z=self.pick_height+5, f=self.fast_speed)
    self.anycubic.move_axis(z=self.pick_height, f=self.slow_speed)
    self.anycubic.finish_request()
    
    while not self.anycubic.get_finish_flag():
        if self.state is not PICK:
            return
        
    # Pumping
    
    self.dyna.write_profile_velocity(self.pipette_fill_speed, ID = 1)
    self.dyna.write_position(self.dyna.pipette(30), ID = 1)
    
    while not self.dyna.pipette_is_in_position(30, ID = 1):
        if self.state is not PICK:
            return
    
    # Check ....
    # cv.check_pickup(frame, self.detector)
    
    # Place
    
    self.state = PLACE
    
def destination(self):
    
    mod = int(self.nb_sample/self.nb_pos[1])
    
    # print('Tube n° ', self.number_sample)
    # print('x offset', mod)
    # print('y offset', self.number_sample%self.num_y)
    
    return round(self.dropping_pos[0]-self.offset_pos*mod, 2), round(self.dropping_pos[1]-self.offset_pos*(self.nb_sample%self.nb_pos[1]), 2)
    
                
    
def place(self):
    
    # Go to position

    self.anycubic.move_axis(z=self.safe_height, f=self.medium_speed)
    dest_x, dest_y = destination(self=self)
    self.anycubic.move_axis(x=dest_x, y=dest_y, f=self.medium_speed)
    self.anycubic.move_axis(z=self.drop_height, f=self.slow_speed)
    self.anycubic.finish_request()
    
    while not self.anycubic.get_finish_flag():
        if self.state is not PLACE:
            return
        
    # Drop
        
    self.dyna.write_profile_velocity(self.pipette_empty_speed, ID = 1)
    self.dyna.write_position(self.dyna.pipette(50), ID = 1)
    
    while not self.dyna.pipette_is_in_position(50, ID = 1):
        if self.state is not PLACE:
            return
        
    # Go up
    
    self.anycubic.move_axis(z=self.safe_height, f=self.fast_speed)
    self.anycubic.finish_request()
    
    while not self.anycubic.get_finish_flag():
        if self.state is not PLACE:
            return
        
    # Reset
    
    self.state = RESET
 