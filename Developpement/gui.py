import cv2
import numpy as np

MENU_A = 0
MENU_B = 1
MENU_C = 2
MENU_D = 3
NB_MENU = 4

SUB_MENU_0 = 0
SUB_MENU_1 = 1
SUB_MENU_2 = 2
SUB_MENU_3 = 3
NB_SUB_MENU = [4, 3, 2, 1]

class platform_pick_and_place_gui:
    
    def __init__(self):
        
        # GUI
        self.gui_menu = 0
        self.gui_menu_label = np.array(['Pick height', 'Drop height', 'Slow speed', 'Medium speed', 'Fast speed', 'Pumping Volume', 'Pumping speed', 'Dropping volume', 'Dropping speed'])

        self.pick_height = 2.5
        self.drop_height = 2.5
        self.fast_speed = 5000
        self.medium_speed = 2000
        self.slow_speed = 300

        self.pipette_dropping_speed = 40
        self.pipette_dropping_volume = 10
        self.pipette_pumping_speed = 10
        self.pipette_pumping_volume = 20
        
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
        color = (0, 0, 255) #BGR
        thickness = 2
    
        fontScale = 0.8 
        
        text = self.gui_menu_label[(self.gui_menu)%len(self.gui_menu_label)]
        self.frame = cv2.putText(self.frame, text, position, font, 
                                fontScale, color, thickness, cv2.LINE_AA)  
        
        pos = position
        pos[0] = pos[0] + 250 
        text = str(round(self.parameter(), 2))
        self.frame = cv2.putText(self.frame, text, position, font, 
                                fontScale, color, thickness, cv2.LINE_AA)  
        

    def gui(self, key):
        
        if key == ord('a'):
            self.gui_menu += 1
            if self.gui_menu == len(self.gui_menu_label):
                self.gui_menu = 0
                
        if key == ord('d'):
            self.gui_menu -= 1
            if self.gui_menu < 0:
                self.gui_menu = len(self.gui_menu_label)-1
                
        if key == ord('w'):
            self.parameter('up')
            
        if key == ord('s'):
            self.parameter('down')
                        
        self.display([50, 150])
    
    
plat = platform_pick_and_place_gui()

while True:
        
    plat.frame = np.ones((450,800))

    # Inputs
    key = cv2.waitKey(10) & 0xFF
    
    plat.gui(key)
    cv2.imshow('Camera', plat.frame)     
    
    if key == 27: #esc
        break      
    

cv2.destroyAllWindows()