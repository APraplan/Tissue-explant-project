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

        self.settings["Position"]["Pick height"] = 2.5
        self.settings["Position"]["Drop height"] = 2.5
        self.settings["Speed"]["Fast speed"]= 5000
        self.settings["Speed"]["Medium speed"] = 2000
        self.settings["Speed"]["Slow speed"] = 300

        self.settings["Tissues"]["Dropping speed"] = 40
        self.settings["Tissues"]["Dropping volume"] = 10
        self.settings["Tissues"]["Pumping speed"] = 10
        self.settings["Tissues"]["Pumping Volume"] = 20
        
    def gui_parameter(self, direction=None):
        
        if direction == 'up':
            
            if self.gui_menu == 0:
                self.settings["Position"]["Pick height"] += 0.1
            if self.gui_menu == 1:
                self.settings["Position"]["Drop height"] += 0.1
            if self.gui_menu == 2:
                self.settings["Speed"]["Slow speed"] += 1
            if self.gui_menu == 3:
                self.settings["Speed"]["Medium speed"] += 1
            if self.gui_menu == 4:
                self.settings["Speed"]["Fast speed"]+= 1        
            if self.gui_menu == 5:
                self.settings["Tissues"]["Pumping Volume"] += 1
            if self.gui_menu == 6:
                self.settings["Tissues"]["Pumping speed"] += 1
            if self.gui_menu == 7:
                self.settings["Tissues"]["Dropping volume"] += 1
            if self.gui_menu == 8:
                self.settings["Tissues"]["Dropping speed"] += 1 
        
        if direction == 'down':
            
            if self.gui_menu == 0:
                self.settings["Position"]["Pick height"] -= 0.1
            if self.gui_menu == 1:
                self.settings["Position"]["Drop height"] -= 0.1
            if self.gui_menu == 2:
                self.settings["Speed"]["Slow speed"] -= 1
            if self.gui_menu == 3:
                self.settings["Speed"]["Medium speed"] -= 1
            if self.gui_menu == 4:
                self.settings["Speed"]["Fast speed"]-= 1        
            if self.gui_menu == 5:
                self.settings["Tissues"]["Pumping Volume"] -= 1
            if self.gui_menu == 6:
                self.settings["Tissues"]["Pumping speed"] -= 1
            if self.gui_menu == 7:
                self.settings["Tissues"]["Dropping volume"] -= 1
            if self.gui_menu == 8:
                self.settings["Tissues"]["Dropping speed"] -= 1 
                
        if direction is None:
            
            if self.gui_menu == 0:
                return self.settings["Position"]["Pick height"]
            if self.gui_menu == 1:
                return self.settings["Position"]["Drop height"]
            if self.gui_menu == 2:
                return self.settings["Speed"]["Slow speed"]
            if self.gui_menu == 3:
                return self.settings["Speed"]["Medium speed"]
            if self.gui_menu == 4:
                return self.settings["Speed"]["Fast speed"]      
            if self.gui_menu == 5:
                return self.settings["Tissues"]["Pumping Volume"]
            if self.gui_menu == 6:
                return self.settings["Tissues"]["Pumping speed"]
            if self.gui_menu == 7:
                return self.settings["Tissues"]["Dropping volume"]
            if self.gui_menu == 8:
                return self.settings["Tissues"]["Dropping speed"]
                
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
        # Left: 2424832 Up: 2490368 Right: 2555904 Down: 2621440
        
        if key == 2424832:#ord('a'):
            print("test")
            self.gui_menu += 1
            if self.gui_menu == len(self.gui_menu_label):
                self.gui_menu = 0
                
        if key == 2555904:#ord('d'):
            self.gui_menu -= 1
            if self.gui_menu < 0:
                self.gui_menu = len(self.gui_menu_label)-1
                
        if key == 2490368: #ord('w'):
            self.parameter('up')
            
        if key == 2621440:#ord('s'):
            self.parameter('down')
                        
        self.display([50, 150])
    
    
plat = platform_pick_and_place_gui()

while True:
        
    plat.frame = np.ones((450,800))

    # Inputs
    key = cv2.waitKeyEx(10)
    
    plat.gui(key)
    cv2.imshow('Camera', plat.frame)     
    
    if key == 27: #esc
        break      
    

cv2.destroyAllWindows()