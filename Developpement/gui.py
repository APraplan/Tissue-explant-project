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
        self.gui_sub_menu = np.array([[0, 0, 0, 0, 0],
                                      [2, 2, 2, 2, 2]])
        self.gui_labels_Status = ['Status', 'State']
        self.gui_labels_Vsion = ['Vision', 'Size max', 'Size min']
        
        self.state = 'pause'
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
        # self.anycubic = printer(descriptive_device_name="printer", port_name="COM10", baudrate=115200)
        self.fast_speed = 5000
        self.medium_speed = 2000
        self.slow_speed = 300
        
        # Dynamixel
        # self.dyna = Dynamixel(ID=[1], descriptive_device_name="XL430 test motor", series_name=["xl"], baudrate=57600,
                #  port_name="COM12")
        self.pipette_empty_speed = 100
        self.pipette_fill_speed = 10
        
        # Tissues
        self.nb_sample = 0
        self.sample_list = []
        
        # Camera
        # self.detector = cv.create_detector() 
        # self.mask = cv.create_mask(200, (cv.HEIGHT_PX, cv.WIDTH_PX), (cv.WIDTH_PX//2, cv.HEIGHT_PX//2))
        self.frame = np.zeros((450, 800))
        self.detect_attempt = 0
        self.max_attempt = 50

    def display(self):
        
        font = cv2.FONT_HERSHEY_SIMPLEX
        color = (255, 255, 255) #BGR
        thickness = 2
        
        if self.gui_menu == 0:
            sub_menu = self.gui_labels_Status
        else:
            sub_menu = self.gui_labels_vision
        
        for num in range(len(sub_menu)):
            position = (30, 30+30*num)
            text =  sub_menu[num]
            if num == self.gui_sub_menu[self.gui_menu, 0]:
                        fontScale = 1.3
            else:
                fontScale = 1
                
            # size, _ = cv2.getTextSize(text, font, fontScale, thickness)a
            self.frame = cv2.putText(self.frame, text, position, font, 
                        fontScale, color, thickness, cv2.LINE_AA)    
        

    def gui(self, key):
        
        if self.gui_sub_menu[self.gui_menu, 0] == 0:
            if key == ord('d'):
                self.gui_menu += 1
                if self.gui_menu == self.gui_sub_menu.shape[2]:
                    gui_state = 0
                    
            if key == ord('a'):
                self.gui_menu -= 1
                if self.gui_menu < 0:
                    self.gui_menu = self.gui_sub_menu.shape[2]-1
                
        self.display()

                
        # if key == ord('a'):
        #     gui_sub_state[gui_state] += 1
        #     if gui_sub_state[gui_state] == NB_SUB_MENU[gui_state]:
        #         gui_sub_state[gui_state] = 0
                
        # if key == ord('d'):
        #     gui_sub_state[gui_state] -= 1
        #     if gui_sub_state[gui_state] < 0:
        #         gui_sub_state[gui_state] = NB_SUB_MENU[gui_state]-1
        
        # frame = display(frame, gui_state, gui_sub_state)
            
        # return frame, gui_state, gui_sub_state
    
    
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