import cv2
import numpy as np

    
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


def display_state_from_dev(imshow, position):
    
    state = 'Idle'
    sub_state = 'Idle'
    well_num = 0
    nb_sample = 0
    nb_sample_remaning = 345
    success = True
    bbox = (0, 0, 2, 2)
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 0.8
    color = (0.9*250, 0.9*250, 0.9*250) #BGR
    thickness = 1
    
    # Print state
    text = state
    pos = list(position)
    # size, _ = cv2.getTextSize(text, font, fontScale, thickness)
    imshow = cv2.putText(imshow, text, pos, font, 
                fontScale, color, thickness, cv2.LINE_AA)    
    
    text = sub_state
    pos[1] += 40
    # size, _ = cv2.getTextSize(text, font, fontScale, thickness)
    imshow = cv2.putText(imshow, text, pos, font, 
                fontScale, color, thickness, cv2.LINE_AA)   
    
    text = 'Number of well ' + str(well_num) 
    pos[1] += 40
    imshow = cv2.putText(imshow, text, pos, font, 
                fontScale, color, thickness, cv2.LINE_AA)
    
    text = 'Number of sample ' + str(nb_sample) 
    pos[1] += 40
    imshow = cv2.putText(imshow, text, pos, font, 
                fontScale, color, thickness, cv2.LINE_AA)
    
    # text = 'Remaning samples ' + str(nb_sample_remaning) 
    # pos[1] += 40
    # imshow = cv2.putText(imshow, text, pos, font, 
    #             fontScale, color, thickness, cv2.LINE_AA)
    
    if success:
        x, y, w, h = [int(i) for i in bbox]
        offset = 500, 165
        cv2.circle(imshow, (int(x+w/2+offset[0]), int(y+h/2+offset[1])), int((w+h)/4), (255, 0, 0), 2)
        # cv2.rectangle(imshow, (x, y), (x + w, y + h), (0, 0, 255), 2)


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
    
    if self.success:
        x, y, w, h = [int(i) for i in self.bbox]
        offset = 500, 165
        cv2.circle(imshow, (int(x+w/2+offset[0]), int(y+h/2+offset[1])), int((w+h)/4), (255, 0, 0), 2)
        # cv2.rectangle(imshow, (x, y), (x + w, y + h), (0, 0, 255), 2)
        
    return imshow


def display_gui_txt(self, imshow, position):
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    color = (0.9*250, 0.9*250, 0.9*250) #BGR
    thickness = 1

    fontScale = 0.8 
    
    pos = list(position)
    
    name, unit = self.gui_menu_label[(self.gui_menu)%len(self.gui_menu_label), 0], self.gui_menu_label[(self.gui_menu)%len(self.gui_menu_label), 1]
    imshow = cv2.putText(imshow, name, pos, font, 
                            fontScale, color, thickness, cv2.LINE_AA)  
    
    pos[0] += 355 
    
    if self.gui_menu == 19:
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
        self.gui_menu += 1
        if self.gui_menu == len(self.gui_menu_label):
            self.gui_menu = 0
            
    if key == ord('d'):
        self.gui_menu -= 1
        if self.gui_menu < 0:
            self.gui_menu = len(self.gui_menu_label)-1
            
    if key == ord('w'):
        gui_parameter(self, 'up')
        
    if key == ord('s'):
        gui_parameter(self, 'down')
                    
    return display_gui_txt(self, imshow, position)
        
    
def display(self, key):
    
    imshow = self.background.copy()
    
    cam = self.frame.copy()
    cam = cv2.resize(cam, (640, 360))
    cam[self.round_edges_mask==1] = 0.2*255
    
    offset = 165, 500
    size = cam.shape
    imshow[offset[0]:offset[0]+size[0], offset[1]:offset[1]+size[1], :] = cam
    
    imshow = display_gui(self, imshow, key, (25, 400))
    imshow = display_state(self, imshow, (25, 200))
    
    return imshow
     
    
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