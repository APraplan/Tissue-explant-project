import cv2
import numpy as np
import pickle
import tensorflow as tf
from keras.models import load_model
import computer_vision as cv
import json

def calibration_sequence(self):

    # Macro camera calibration
    self.anycubic.move_axis_relative(z=self.safe_height, offset=self.settings["Offset"]["Tip one"])
    self.anycubic.move_axis_relative(x=self.picture_pos, offset=self.settings["Offset"]["Tip one"])
    
    while True:
    
        self.macro_frame = self.stream2.read()            

        # Inputs
        key = cv2.waitKey(5) & 0xFF 
        
        if key == 13: #enter
            break
        
        cv2.imshow('Macro camera', self.macro_frame) 
        
    cv2.destroyAllWindows()  
        
        
    # Offset first tip calibration
    self.anycubic.move_axis_relative(z=5, offset=self.settings["Offset"]["Tip one"])
    self.anycubic.move_axis_relative(x=self.settings["Offset"]["Calibration point"][0], y=self.settings["Offset"]["Calibration point"][1], offset=self.settings["Offset"]["Tip one"])
    self.anycubic.move_axis_relative(z=self.settings["Offset"]["Calibration point"][2], offset=self.settings["Offset"]["Tip one"])
    
    while True:
    
        frame = self.stream1.read() 
        self.frame = self.cam.undistort(frame)
        self.invert = cv.invert(self.frame)
        imshow = self.frame.copy()
        
        # self.macro_frame = self.stream2.read()
            
        # Inputs
        key = cv2.waitKey(5) & 0xFF 
        
        self.settings["Offset"]["Tip one"] = calibration_process(self, key, self.settings["Offset"]["Tip one"])
        
        if key == 13: #enter
            print("Offset tip one: ", self.settings["Offset"]["Tip one"])
            break
        
        cv2.imshow('Camera', imshow) 
        
        
    # Change tip
    self.anycubic.move_axis_relative(z=self.safe_height, offset=self.settings["Offset"]["Tip one"])
    self.anycubic.finish_request()
    while not self.anycubic.get_finish_flag():
        frame = self.stream1.read() 
        self.frame = self.cam.undistort(frame)
        imshow = self.frame.copy()

        cv2.imshow('Camera', imshow) 
        
    self.tip_number = 2
    self.dyna.select_tip(tip_number=self.tip_number, ID=3)
        
            
    # Offset second tip calibration
    self.anycubic.move_axis_relative(x=self.settings["Offset"]["Calibration point"][0], y=self.settings["Offset"]["Calibration point"][1], offset=self.settings["Offset"]["Tip two"])
    self.anycubic.move_axis_relative(z=self.settings["Offset"]["Calibration point"][2], offset=self.settings["Offset"]["Tip two"])
    
    while True:
    
        frame = self.stream1.read() 
        self.frame = self.cam.undistort(frame)
        self.invert = cv.invert(self.frame)
        imshow = self.frame.copy()
        
        # self.macro_frame = self.stream2.read()
            
        # Inputs
        key = cv2.waitKey(5) & 0xFF 
        
        self.settings["Offset"]["Tip two"] = calibration_process(self, key, self.settings["Offset"]["Tip two"])
        
        if key == 13: #enter
            print("Offset tip two: ", self.settings["Offset"]["Tip two"])
            break
            
        cv2.imshow('Camera', imshow) 
        
    # Change tip
    self.anycubic.move_axis_relative(z=self.safe_height, offset=self.settings["Offset"]["Tip one"])
    self.anycubic.finish_request()
    while not self.anycubic.get_finish_flag():
        frame = self.stream1.read() 
        self.frame = self.cam.undistort(frame)
        imshow = self.frame.copy()

        cv2.imshow('Camera', imshow) 
        
    self.tip_number = 1
    self.dyna.select_tip(tip_number=self.tip_number, ID=3)
        
    # Offset camera calibration
    self.anycubic.move_axis_relative(x=self.settings["Offset"]["Calibration point"][0], y=self.settings["Offset"]["Calibration point"][1], offset=self.settings["Offset"]["Camera"])
    self.anycubic.move_axis_relative(z=self.safe_height, offset=self.settings["Offset"]["Camera"])
    
    while True:
    
        frame = self.stream1.read() 
        self.frame = self.cam.undistort(frame)
        self.invert = cv.invert(self.frame)
        imshow = self.frame.copy()
        
        # self.macro_frame = self.stream2.read()
            
        # Inputs
        key = cv2.waitKey(5) & 0xFF 
        
        offset = self.settings["Offset"]["Camera"]
        offset[2] += self.safe_height
        offset = calibration_process(self, key, offset)
        self.settings["Offset"]["Camera"][2] = 0
        
        if key == 13: #enter
            print("Offset cam: ", self.settings["Offset"]["Camera"])
            break
        
        markerSize = 15
        thickness = 1
        center = (imshow.shape[1]//2, imshow.shape[0]//2)
        imshow = cv2.drawMarker(imshow, center, (255, 0, 0), cv2.MARKER_CROSS, markerSize, thickness)
        
        cv2.imshow('Camera', imshow) 

    
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
            
        if self.gui_menu == 9:
            self.settings["Solution A"]["Solution A pumping speed"] += 1
        if self.gui_menu == 10:
            self.settings["Solution A"]["Solution A dropping speed"] += 1
        if self.gui_menu == 11:
            self.settings["Solution A"]["Solution A pumping volume"] += 1
        if self.gui_menu == 12:
            self.settings["Solution B"]["Solution B pumping speed"] += 1
        if self.gui_menu == 13:
            self.settings["Solution B"]["Solution B dropping speed"] += 1
        if self.gui_menu == 14:
            self.settings["Solution B"]["Solution B pumping volume"] += 1
        if self.gui_menu == 15:
            self.settings["Gel"]["Tube pumping height"] += 0.1
        if self.gui_menu == 16:
            self.settings["Gel"]["Vial pumping height"] += 0.1
        if self.gui_menu == 17:
            self.settings["Gel"]["Well plate pumping height"] += 0.1
        if self.gui_menu == 18:
            if self.settings["Gel"]["Number of mix"] < 10:
                self.settings["Gel"]["Number of mix"]  += 1
        if self.gui_menu == 19:
            if self.settings["Gel"]["Number of wash"] < 10:
                self.settings["Gel"]["Number of wash"] += 1
        if self.gui_menu == 20:
            self.settings["Detection"]["Max attempt"] += 1
        if self.gui_menu == 21:
            if self.settings["Detection"]["Size min"] < self.settings["Detection"]["Size max"]:
                self.settings["Detection"]["Size min"] += 1
        if self.gui_menu == 22:
            if self.settings["Detection"]["Size max"] < 200:
                self.settings["Detection"]["Size max"] += 1
        if self.gui_menu == 23:
            self.settings["Well"]["Well preparation"] = True
        if self.gui_menu == 24:
            if self.settings["Well"]["Type"] == "TPP6":
                self.settings["Well"]["Type"] = "TPP12"
            elif self.settings["Well"]["Type"] == "TPP12":
                self.settings["Well"]["Type"] = "TPP24"
            elif self.settings["Well"]["Type"] == "TPP24":
                self.settings["Well"]["Type"] = "TPP48"
        if self.gui_menu == 25:
            if self.settings["Well"]["Number of sample per well"] < 8:
                self.settings["Well"]["Number of sample per well"] += 1
        if self.gui_menu == 26:
            if self.settings["Well"]["Number of well"] < 6:
                self.settings["Well"]["Number of well"] += 1
    
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
            
        if self.gui_menu == 9:
            self.settings["Solution A"]["Solution A pumping speed"] -= 1
        if self.gui_menu == 10:
            self.settings["Solution A"]["Solution A dropping speed"] -= 1
        if self.gui_menu == 11:
            self.settings["Solution A"]["Solution A pumping volume"] -= 1
        if self.gui_menu == 12:
            self.settings["Solution B"]["Solution B pumping speed"] -= 1
        if self.gui_menu == 13:
            self.settings["Solution B"]["Solution B dropping speed"] -= 1
        if self.gui_menu == 14:
            self.settings["Solution B"]["Solution B pumping volume"] -= 1
        if self.gui_menu == 15:
            self.settings["Gel"]["Tube pumping height"] -= 0.1
        if self.gui_menu == 16:
            self.settings["Gel"]["Vial pumping height"] -= 0.1
        if self.gui_menu == 17:
            self.settings["Gel"]["Well plate pumping height"] -= 0.1
        if self.gui_menu == 18:
            if self.settings["Gel"]["Number of mix"] > 0:
                self.settings["Gel"]["Number of mix"]  -= 1
        if self.gui_menu == 19:
            if self.settings["Gel"]["Number of wash"] > 0:
                self.settings["Gel"]["Number of wash"] -= 1
        if self.gui_menu == 20:
            self.settings["Detection"]["Max attempt"] -= 1
        if self.gui_menu == 21:
            if self.settings["Detection"]["Size min"] > 0:
                self.settings["Detection"]["Size min"] -= 1
        if self.gui_menu == 22:
            if self.settings["Detection"]["Size max"] > self.settings["Detection"]["Size min"]:
                self.settings["Detection"]["Size max"] -= 1
        if self.gui_menu == 23:
            self.settings["Well"]["Well preparation"] = False
        if self.gui_menu == 24:
            if self.settings["Well"]["Type"] == "TPP48":
                self.settings["Well"]["Type"] = "TPP24"
            elif self.settings["Well"]["Type"] == "TPP24":
                self.settings["Well"]["Type"] = "TPP12"
            elif self.settings["Well"]["Type"] == "TPP12":
                self.settings["Well"]["Type"] = "TPP6"
        if self.gui_menu == 25:
            if self.settings["Well"]["Number of sample per well"] > 1:
                self.settings["Well"]["Number of sample per well"] -= 1
        if self.gui_menu == 26:
            if self.settings["Well"]["Number of well"] > 1:
                self.settings["Well"]["Number of well"] -= 1
            
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
        
        if self.gui_menu == 9:
            return self.settings["Solution A"]["Solution A pumping speed"]
        if self.gui_menu == 10:
            return self.settings["Solution A"]["Solution A dropping speed"]
        if self.gui_menu == 11:
            return self.settings["Solution A"]["Solution A pumping volume"]
        if self.gui_menu == 12:
            return self.settings["Solution B"]["Solution B pumping speed"]
        if self.gui_menu == 13:
            return self.settings["Solution B"]["Solution B dropping speed"]
        if self.gui_menu == 14:
            return self.settings["Solution B"]["Solution B pumping volume"]
        if self.gui_menu == 15:
            return self.settings["Gel"]["Tube pumping height"]
        if self.gui_menu == 16:
            return self.settings["Gel"]["Vial pumping height"]
        if self.gui_menu == 17:
            return self.settings["Gel"]["Well plate pumping height"]
        if self.gui_menu == 18:
            return self.settings["Gel"]["Number of mix"]
        if self.gui_menu == 19:
            return self.settings["Gel"]["Number of wash"]
        if self.gui_menu == 20:
            return self.settings["Detection"]["Max attempt"]  
        if self.gui_menu == 21:
            return self.settings["Detection"]["Size min"]
        if self.gui_menu == 22:
            return self.settings["Detection"]["Size max"]     
        if self.gui_menu == 23:
            if self.settings["Well"]["Well preparation"]:
                return 'yes'
            else:
                return 'no'
        if self.gui_menu == 24:
            return self.settings["Well"]["Type"]
        if self.gui_menu == 25:
            return self.settings["Well"]["Number of sample per well"]
        if self.gui_menu == 26:
            return self.settings["Well"]["Number of well"]


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
    
    if type(gui_parameter(self)) == str:
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
        
    if key == 2424832: #Right
        self.gui_menu -= 1
        if self.gui_menu < 0:
            self.gui_menu = len(self.gui_menu_label)-1
    
    if key == 2555904: #Left
        self.gui_menu += 1
        if self.gui_menu == len(self.gui_menu_label):
            self.gui_menu = 0
            
    if key == 2490368: #Up
        gui_parameter(self, 'up')
        
    if key == 2621440:#Down
        gui_parameter(self, 'down')
                    
    return display_gui_txt(self, imshow, position)
        
    
def display(self, key):
    
    imshow = self.background.copy()
    
    cam = self.frame.copy()
            
    
    cv2.circle(cam, (int(self.tip_pos_px[0]), int(self.tip_pos_px[1])), 5, (0, 0, 255), 2) 
    
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
            
    if key == 2555904: #Left
        offset[0] -= incr
        self.anycubic.move_axis_relative(x=self.settings["Offset"]["Calibration point"][0], 
                                        y=self.settings["Offset"]["Calibration point"][1], 
                                        z=self.settings["Offset"]["Calibration point"][2], offset=offset)
        
    elif key == 2424832: #Right
        offset[0] += incr
        self.anycubic.move_axis_relative(x=self.settings["Offset"]["Calibration point"][0], 
                                        y=self.settings["Offset"]["Calibration point"][1], 
                                        z=self.settings["Offset"]["Calibration point"][2], offset=offset)

    if key == 2490368: #Up
        offset[1] += incr
        self.anycubic.move_axis_relative(x=self.settings["Offset"]["Calibration point"][0], 
                                        y=self.settings["Offset"]["Calibration point"][1], 
                                        z=self.settings["Offset"]["Calibration point"][2], offset=offset)

    if key == 2621440:#Down
        offset[1] -= incr
        self.anycubic.move_axis_relative(x=self.settings["Offset"]["Calibration point"][0], 
                                        y=self.settings["Offset"]["Calibration point"][1], 
                                        z=self.settings["Offset"]["Calibration point"][2], offset=offset)

    elif key == ord('e'):
        offset[2] += incr
        self.anycubic.move_axis_relative(x=self.settings["Offset"]["Calibration point"][0], 
                                        y=self.settings["Offset"]["Calibration point"][1], 
                                        z=self.settings["Offset"]["Calibration point"][2], offset=offset)

    elif key == ord('c'):
        offset[2] -= incr
        self.anycubic.move_axis_relative(x=self.settings["Offset"]["Calibration point"][0], 
                                        y=self.settings["Offset"]["Calibration point"][1], 
                                        z=self.settings["Offset"]["Calibration point"][2], offset=offset)

    return offset
    
    
def save_parameters(self):
    
    with open("settings.json", "w") as jsonFile:
        json.dump(self.settings, jsonFile, indent=4)
    
    
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
                                    ['Gel', "Tube pumping height", "mm"], ["Gel", "Vial pumping height", "mm"], ["Gel", "Well plate pumping height", "mm"], ['Gel', 'Number of mix', ''], ['Gel', 'Number of wash', ''],
                                    ['Detection', 'Max attempt', ''],['Detection', 'Size min', ''], ['Detection', 'Size max', ''],
                                    ['Well', 'Well prepatation', ''], ["Well", "Type", ""], ['Well', 'Number of sample per well', ''], ['Well', 'Number of well', '']])
    
    with open("settings.json", "r") as jsonFile:
        self.settings = json.load(jsonFile)
        
    
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