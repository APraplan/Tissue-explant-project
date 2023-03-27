import numpy as np
import computer_vision as cv
import cv2

# PETRI_DISH_HEIGHT = 25
# PETRI_DISH_PICK_HEIGHT = 0.8
# PETRI_DISH_X_POSITION = 50
# PETRI_DISH_Y_POSITION = 100
# PETRI_DISH_RADIUS = 45

# TEST_TUBE_HEIGHT = 10
# TEST_TUBE_PLACE_HEIGHT = 3
# TEST_TUBE_X_POSITION = 180
# TEST_TUBE_Y_POSITION = 160
# TEST_TUBE_X_MIN = 105
# TEST_TUBE_X_MAX = 195
# TEST_TUBE_Y_MIN = 45
# TEST_TUBE_Y_MAX = 175
# NUMBER_TUBE_X = 8
# NUMBER_TUBE_Y = 12
# OFFSET_TUBE = 8.2


# TEST_TUBE_N = np.array([1, 0, 0])
# TEST_TUBE_P0 = np.array([TEST_TUBE_X_MIN, 0, 0])


class sample:
    
    def __init__(self, num, x, y, image = None):
        self.num = num
        self.x = x
        self.y = y
        self.image = None


class platform_pick_and_place:
    
    def __init__(self, anycubic, dynamixel, detector):
        self.state = 'reset'
        self.last_state = 'reset'
        self.sub_state = 'go to position'
        self.com_state = 'not send'
        
        # Picking zone
        self.safe_height = 25
        self.pick_height = 3.2
        self.detection_place = [75.0, 125, 50]
        self.reset_pos = [90, 115, 10]
                
        # Dropping zone
        self.dropping_pos = [180, 160]
        self.nb_pos = [8, 12]
        self.offset_pos = 8.2
        self.drop_height = 3.5
        
        # Anycubic
        self.anycubic = anycubic
        self.fast_speed = 5000
        self.medium_speed = 2000
        self.slow_speed = 300
        
        # Dynamixel
        self.dyna = dynamixel
        self.pipette_empty_speed = 100
        self.pipette_fill_speed = 10
        
        # Tissues
        self.nb_sample = 0
        self.sample_list = []
        
        # Camera
        self.detector = detector 
        self.mask = cv.create_mask(200, (427, 603), (301, 213))
        self.detect_attempt = 0
        self.max_attempt = 50
        
             
    # Private methodes
                
    def __destination(self):
        
        mod = int(self.nb_sample/self.nb_pos[1])
        
        # print('Tube n° ', self.number_sample)
        # print('x offset', mod)
        # print('y offset', self.number_sample%self.num_y)
        
        return round(self.dropping_pos[0]-self.offset_pos*mod, 2), round(self.dropping_pos[1]-self.offset_pos*(self.nb_sample%self.nb_pos[1]), 2)
    
    
    def __detect(self, frame):
        
  
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
            
            target =  cv.detect(frame, self.detection_place, self.detector, self.mask)
            
            if target is not None:
                self.sample_list.append(sample(self.nb_sample, target[0], target[1]))
                self.nb_sample += 1
            
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
       
        
    def __pick(self, frame):
                
        
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
                self.anycubic.move_axis(x=self.sample_list[self.nb_sample-1].x, y=self.sample_list[self.nb_sample-1].y, f=self.slow_speed)
                self.anycubic.move_axis(z=self.pick_height, f=self.slow_speed)
                self.anycubic.finish_request()
                self.com_state = 'send'
               
            elif self.anycubic.get_finish_flag():
                self.sub_state = 'suck'
                self.com_state = 'not send'
                
   
        elif self.sub_state == 'suck':
            
            if self.com_state == 'not send':
                self.dyna.write_profile_velocity(self.pipette_fill_speed, ID = 1)
                self.dyna.write_position(self.dyna.pipette(30), ID = 1)
                self.com_state = 'send'
                
            elif self.dyna.pipette_is_in_position(30, ID = 1):
                self.sub_state = 'check'
                self.com_state = 'not send'
                
        
        elif self.sub_state == 'check':
            
            if self.sub_state == 'not send':
                self.anycubic.move_axis(z=self.safe_height, f=self.medium_speed)
                self.anycubic.finish_request()
                self.com_state = 'send'
               
            elif self.anycubic.get_finish_flag():
                
                if cv.check_pickup(frame, self.detector):
                    self.state = 'place'
                    self.sub_state = 'go to position'
                    self.com_state = 'not send'    
                else:
                    self.state = 'reset'
                    self.sub_state = 'go to position'
                    self.com_state = 'not send'
                    
                
    
    def __place(self, frame):

        if self.sub_state == 'go to position':
            
            if self.com_state == 'not send':
                self.anycubic.move_axis(z=self.safe_height, f=self.medium_speed)
                dest_x, dest_y = self.__destination()
                self.anycubic.move_axis(x=dest_x, y=dest_y, f=self.medium_speed)
                self.anycubic.finish_request()
                self.com_state = 'send'
               
            elif self.anycubic.get_finish_flag():
                self.sub_state = 'check'
                self.com_state = 'not send'       
                
                
        elif self.sub_state == 'check':
               
            if cv.check_pickup(frame, self.detector):
                self.sub_state = 'go down'    
            else: 
                self.state = 'reset'
                self.sub_state = 'go to position'
                self.com_state = 'send'
                
       
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
                self.dyna.write_position(self.dyna.pipette(50), ID = 1)
                self.com_state = 'send'
                
            elif self.dyna.pipette_is_in_position(50, ID = 1):
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
                
    
    def __reset(self):
        
    
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
                      
    
    # Public methodes
    
    def run(self, frame):
            
        if self.state == 'detect':
            self.__detect(frame=frame)
            
        elif self.state == 'pick':
            self.__pick(frame=frame)
            
        elif self.state == 'place':
            self.__place(frame=frame)           
            
        elif self.state == 'reset':
            self.__reset()  
        
     
    def pause(self):
    
        if self.state != 'pause':
            self.last_state = self.state
            self.state = 'pause'
            
            
    def resume(self):
        
        if self.state == 'pause':
            self.state = self.last_state
                

    def reset(self):
        
        # if self.state != 'reset':
            self.state = 'reset'
            self.sub_state = 'go to position'
            self.com_state = 'not send'
            
            
    def get_sample(self):
        
        return self.sample_list, self.nb_sample
    
    
    def print(self, image):
        
        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 0.8
        color = (255, 255, 255) #BGR
        thickness = 2
        
        # Print state
        text = self.state
        position = (20, 20)
        # size, _ = cv2.getTextSize(text, font, fontScale, thickness)
        out = cv2.putText(image, text, position, font, 
                   fontScale, color, thickness, cv2.LINE_AA)    
        
        text = self.sub_state
        position = (20, 50)
        # size, _ = cv2.getTextSize(text, font, fontScale, thickness)
        out = cv2.putText(image, text, position, font, 
                   fontScale, color, thickness, cv2.LINE_AA)       
        
        return image

        
        
        
        
        
        
        
        
        
        
        
        
        
    # def add_one_sample(self):
    #     self.number_sample += 1

        
# class petri_dish:
#     def __init__(self, x, y, z, pick_z, r):
#         self.x = x
#         self.y = y
#         self.z = z 
#         self.pick_z = pick_z
#         self.r = r 
        
# class test_tube:
#     def __init__(self, x1, y1, z, place_z, min_x, max_x, min_y, max_y, num_x, num_y, offset_tube):
#         self.x1 = x1
#         self.y1 = y1
#         self.z = z
#         self.place_z = place_z
#         self.min_x = min_x
#         self.max_x = max_x
#         self.min_y = min_y 
#         self.max_y = max_y
#         self.num_x = num_x
#         self.num_y = num_y 
#         self.offset_tube = offset_tube
#         self.number_sample = 0
    
#     def destination(self):
#         mod = int(self.number_sample/self.num_y)
        
#         print('Tube n° ', self.number_sample)
#         print('x offset', mod)
#         print('y offset', self.number_sample%self.num_y)
        
#         if mod == self.num_x -1:
#             print('Test tube full !')
#             return 
#         else:
#             return self.x1-self.offset_tube*mod, self.y1-self.offset_tube*(self.number_sample%self.num_y)
        
#     def add_one_sample(self):
#         self.number_sample += 1
        

# petri = petri_dish(PETRI_DISH_X_POSITION, PETRI_DISH_Y_POSITION, PETRI_DISH_HEIGHT, PETRI_DISH_PICK_HEIGHT, PETRI_DISH_RADIUS) 

# tube = test_tube(TEST_TUBE_X_POSITION, TEST_TUBE_Y_POSITION, TEST_TUBE_HEIGHT, TEST_TUBE_PLACE_HEIGHT, TEST_TUBE_X_MIN, TEST_TUBE_X_MAX, TEST_TUBE_Y_MIN, TEST_TUBE_Y_MAX, NUMBER_TUBE_X, NUMBER_TUBE_Y, OFFSET_TUBE)   
        