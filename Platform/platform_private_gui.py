import cv2
import numpy as np
import pickle
import tensorflow as tf
from keras.models import load_model

    
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
            
        if self.gui_menu == 9:
            self.solution_A_pumping_speed += 1
        if self.gui_menu == 10:
            self.solution_A_dropping_speed += 1
        if self.gui_menu == 11:
            self.solution_A_pumping_volume += 1
        if self.gui_menu == 12:
            self.solution_B_pumping_speed += 1
        if self.gui_menu == 13:
            self.solution_B_dropping_speed += 1
        if self.gui_menu == 14:
            self.solution_B_pumping_volume += 1
        if self.gui_menu == 15:
            self.solution_pumping_height += 0.1
        if self.gui_menu == 16:
            if self.num_mix < 10:
                self.num_mix  += 1
        if self.gui_menu == 17:
            if self.num_wash < 10:
                self.num_wash += 1
        if self.gui_menu == 18:
            self.max_attempt += 1
        if self.gui_menu == 19:
            if self.min_size < self.max_size:
                self.min_size += 1
        if self.gui_menu == 20:
            if self.max_size < 200:
                self.max_size += 1
        if self.gui_menu == 21:
            self.well_preparation = True
        if self.gui_menu == 22:
            if self.nb_sample_well < 8:
                self.nb_sample_well += 1
        if self.gui_menu == 23:
            if self.number_of_well < 6:
                self.number_of_well += 1
    
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
            
        if self.gui_menu == 9:
            self.solution_A_pumping_speed -= 1
        if self.gui_menu == 10:
            self.solution_A_dropping_speed -= 1
        if self.gui_menu == 11:
            self.solution_A_pumping_volume -= 1
        if self.gui_menu == 12:
            self.solution_B_pumping_speed -= 1
        if self.gui_menu == 13:
            self.solution_B_dropping_speed -= 1
        if self.gui_menu == 14:
            self.solution_B_pumping_volume -= 1
        if self.gui_menu == 15:
            self.solution_pumping_height -= 0.1 
        if self.gui_menu == 16:
            if self.num_mix > 0:
                self.num_mix  -= 1
        if self.gui_menu == 17:
            if self.num_wash > 0:
                self.num_wash -= 1
        if self.gui_menu == 18:
            self.max_attempt -= 1
        if self.gui_menu == 19:
            if self.min_size > 0:
                self.min_size -= 1
        if self.gui_menu == 20:
            if self.max_size > self.min_size:
                self.max_size -= 1
        if self.gui_menu == 21:
            self.well_preparation = False
        if self.gui_menu == 22:
            if self.nb_sample_well > 1:
                self.nb_sample_well -= 1
        if self.gui_menu == 23:
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
            return self.solution_A_pumping_speed
        if self.gui_menu == 10:
            return self.solution_A_dropping_speed
        if self.gui_menu == 11:
            return self.solution_A_pumping_volume
        if self.gui_menu == 12:
            return self.solution_B_pumping_speed
        if self.gui_menu == 13:
            return self.solution_B_dropping_speed
        if self.gui_menu == 14:
            return self.solution_B_pumping_volume
        if self.gui_menu == 15:
            return self.solution_pumping_height
        if self.gui_menu == 16:
            return self.num_mix
        if self.gui_menu == 17:
            return self.num_wash
        if self.gui_menu == 18:
            return self.max_attempt  
        if self.gui_menu == 19:
            return self.min_size
        if self.gui_menu == 20:
            return self.max_size     
        if self.gui_menu == 21:
            if self.well_preparation:
                return 'yes'
            else:
                return 'no'
        if self.gui_menu == 22:
            return self.nb_sample_well
        if self.gui_menu == 23:
            return self.number_of_well


def display_state(self, imshow, position):
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 0.8
    color = (0.9*250, 0.9*250, 0.9*250) #BGR
    thickness = 1
    
    # Print state
    text = self.state
    pos = list(position)
    # size, _ = cv2.getTextSize(text, font, fontScale, thickness)
    imshow = cv2.putText(imshow, text, pos, font, 
                fontScale, color, thickness, cv2.LINE_AA)    
    
    text = self.sub_state
    pos[1] += 40
    # size, _ = cv2.getTextSize(text, font, fontScale, thickness)
    imshow = cv2.putText(imshow, text, pos, font, 
                fontScale, color, thickness, cv2.LINE_AA)   
    
    text = 'Nb well ' + str(self.well_num) 
    pos[1] += 40
    imshow = cv2.putText(imshow, text, pos, font, 
                fontScale, color, thickness, cv2.LINE_AA)
    
    text = 'Nb sample ' + str(self.nb_sample) 
    pos[1] += 40  
    imshow = cv2.putText(imshow, text, pos, font, 
                fontScale, color, thickness, cv2.LINE_AA)
        
    return imshow


def display_gui_txt(self, imshow, position):
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    color = (0.9*250, 0.9*250, 0.9*250) #BGR
    thickness = 1

    fontScale = 0.8 
    
    pos = list(position)
    
    cat, name, unit = self.gui_menu_label[(self.gui_menu)%len(self.gui_menu_label), 0], self.gui_menu_label[(self.gui_menu)%len(self.gui_menu_label), 1], self.gui_menu_label[(self.gui_menu)%len(self.gui_menu_label), 2]
    
    imshow = cv2.putText(imshow, cat, pos, font, 
                            fontScale, color, thickness, cv2.LINE_AA) 
    
    pos[1] += 40
    imshow = cv2.putText(imshow, name, pos, font, 
                            fontScale, color, thickness, cv2.LINE_AA)  
    
    size, _ = cv2.getTextSize(name, font, fontScale, thickness)
    pos[0] += size[0] + 7
    
    if self.gui_menu == 21:
        val = gui_parameter(self)
    else:
        val = str(round(gui_parameter(self), 2))
        
    imshow = cv2.putText(imshow, val, pos, font, 
                            fontScale, color, thickness, cv2.LINE_AA)    
    
    size, _ = cv2.getTextSize(val, font, fontScale, thickness)
    pos[0] += size[0] + 7
    imshow = cv2.putText(imshow, unit, pos, font, 
                            fontScale, color, thickness, cv2.LINE_AA)  
    
    return imshow


def display_gui(self, imshow, key, position):
    
    # if key == ord('c'):
    #     cv2.imwrite("Pictures\Realsample\image_on_the_go.png", self.frame)
    
    if key == ord('p'):
        self.pause()
    if key == 13: # enter
        self.resume()
    if key == ord('r'):
        self.reset()
        
    if key == ord('a'):
        self.gui_menu -= 1
        if self.gui_menu < 0:
            self.gui_menu = len(self.gui_menu_label)-1
    
    if key == ord('d'):
        self.gui_menu += 1
        if self.gui_menu == len(self.gui_menu_label):
            self.gui_menu = 0
            
    if key == ord('w'):
        gui_parameter(self, 'up')
        
    if key == ord('s'):
        gui_parameter(self, 'down')
                    
    return display_gui_txt(self, imshow, position)
        
    
def display(self, key):
    
    imshow = self.background.copy()
    
    cam = self.frame.copy()
    
    if self.success:
        x, y, w, h = [int(i) for i in self.bbox]
        cv2.circle(cam, (int(x+w/2), int(y+h/2)), int((w+h)/4), (255, 0, 0), 2)
        # cv2.rectangle(imshow, (x, y), (x + w, y + h), (0, 0, 255), 2)
    
    cam = cv2.resize(cam, (640, 360))
    cam[self.round_edges_mask==255] = 0.2*255
    
    offset = 165, 500
    size = cam.shape
    imshow[offset[0]:offset[0]+size[0], offset[1]:offset[1]+size[1], :] = cam
    
    imshow = display_gui(self, imshow, key, (25, 360))
    imshow = display_state(self, imshow, (25, 200))
    
    return imshow

def calibration_process(self, key, offset):
    
    incr = 0.1
            
    if key == ord('a'):
        offset[0] -= incr
        self.anycubic.move_axis(x=offset[0],y=offset[1], z=offset[2], printMsg=False)
        
    if key == ord('d'):
        offset[0] += incr
        self.anycubic.move_axis(x=offset[0],y=offset[1], z=offset[2], printMsg=False)
        
    if key == ord('w'):
        offset[1] += incr
        self.anycubic.move_axis(x=offset[0],y=offset[1], z=offset[2], printMsg=False)
        
    if key == ord('s'):
        offset[1] -= incr
        self.anycubic.move_axis(x=offset[0],y=offset[1], z=offset[2], printMsg=False)
        
    if key == ord('e'):
        offset[2] += incr
        self.anycubic.move_axis(x=offset[0],y=offset[1], z=offset[2], printMsg=False)

    if key == ord('c'):
        offset[2] -= incr
        if offset[2] < 0:
            offset[2] = 0
        self.anycubic.move_axis(x=offset[0],y=offset[1], z=offset[2], printMsg=False)
        
    return offset
    
    
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
    params.append(self.solution_A_pumping_speed)
    params.append(self.solution_A_dropping_speed)
    params.append(self.solution_A_pumping_volume)
    params.append(self.solution_B_pumping_speed)
    params.append(self.solution_B_dropping_speed)
    params.append(self.solution_B_pumping_volume)
    params.append(self.solution_pumping_height)
    params.append(self.num_mix)
    params.append(self.num_wash)
    params.append(self.max_attempt)
    params.append(self.min_size)
    params.append(self.max_size)
    params.append(self.well_preparation)
    params.append(self.nb_sample_well)
    params.append(self.number_of_well)
    params.append(self.offset_tip_one)
    params.append(self.offset_tip_two)
    params.append(self.offset_cam)
                
    pickle.dump(params, open('Platform/Calibration/parameters.pkl', 'wb'))
    
    
def load_parameters(self):
    
    self.NN = load_model(r'TEP_convNN_BW')

    self.background = cv2.imread(r'Pictures\Utils\Backgroud.png')
    self.round_edges_mask = cv2.imread(r'Pictures\Utils\mask_rounded_edges.png')
    self.gui_menu = 0
    
    self.gui_menu_label = np.array([['Position', 'Pick height', 'mm'], ['Position', 'Drop height', 'mm'],
                                    ['Speed', 'Slow speed', 'mm/s'], ['Speed', 'Medium speed', 'mm/s'], ['Speed', 'Fast speed', 'mm/s'],
                                    ['Tissues', 'Pumping Volume', 'ul'], ['Tissues', 'Pumping speed', ''], ['Tissues', 'Dropping volume', 'ul'], ['Tissues', 'Dropping speed', ''],
                                    ['Solution A', 'Pumping speed', ''], ['Solution A', 'Dropping speed', ''], ['Solution A', 'Pumping volume', 'ul'],
                                    ['Solution B', 'Pumping speed', ''], ['Solution B', 'Dropping speed', ''], ['Solution B', 'Pumping volume', 'ul'], 
                                    ['Gel', 'Solution pumping height', 'mm'], ['Gel', 'Number of mix', ''], ['Gel', 'Number of wash', ''],
                                    ['Detection', 'Max attempt', ''],['Detection', 'Size min', ''], ['Detection', 'Size max', ''],
                                    ['Well', 'Well prepatation', ''],
                                    ['Well', 'Number of sample per well', ''],
                                    ['Well', 'Number of well', '']])

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
    self.solution_A_pumping_speed = params[9]
    self.solution_A_dropping_speed = params[10]
    self.solution_A_pumping_volume = params[11]
    self.solution_B_pumping_speed = params[12]
    self.solution_B_dropping_speed = params[13]
    self.solution_B_pumping_volume = params[14]
    self.solution_pumping_height = params[15]
    self.num_mix = params[16]
    self.num_wash = params[17]
    self.max_attempt = params[18]
    self.min_size = params[19]
    self.max_size = params[20]
    self.well_preparation = params[21]
    self.nb_sample_well = params[22]
    self.number_of_well = params[23]
    self.offset_tip_one = params[24]
    self.offset_tip_two = params[25]
    self.offset_cam = params[26]
     
    
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