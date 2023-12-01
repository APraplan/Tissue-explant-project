import tkinter as tk                     
from tkinter import ttk 
import json
import customtkinter as ctk

    
from Platform.Communication.ports_gestion import * # check how to get rid of this warning
import Platform.computer_vision as cv
from PIL import Image, ImageTk
import Developpement.Cam_gear as cam_gear
import cv2

debug = True

if debug:
    from Platform.Communication.fake_communication import * 
else:
    from Platform.Communication.dynamixel_controller import *
    from Platform.Communication.printer_communications import * 
    import Developpement.Cam_gear as cam_gear
    

### ATTENTION AU OFFSET  !!!

SETTINGS = "TEST.json"
X_MIN = 0.0
X_MAX = 145.0
Y_MIN = 0.0
Y_MAX = 145.0
Z_MIN = 0.0
Z_MAX = 180.0

DEFAULT_MODE = "Light"
ctk.set_appearance_mode(DEFAULT_MODE)  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

DARK_COLOR = "#242424"
LIGHT_COLOR = "#ebebeb"

DEFAULT_LIGHT = "#dbdbdb"
DEFAULT_DARK = "#2b2b2b"

class ArrowButtonRight(tk.Frame):  ## replace these with pictures
    def __init__(self, master=None, size=40, target_class=None, printer_class=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        
        self.target_class = target_class
        self.printer_class = printer_class
        self.canvas = tk.Canvas(self, width=size, height=size)
        self.canvas.create_polygon(7, 7, 35, 20, 7, 33, fill="black", outline="black")
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.grid()

    def on_click(self, event):
        if self.target_class.is_homed:
            print("?Moving  "+str(self.target_class.xyz_step), " in X-UP")
            self.target_class.move_xyz(x=self.target_class.xyz_step, y=0, z=0)
        else:
            print("?? Printer not homed yet, please home the printer first")


class ArrowButtonTop(tk.Frame):
    def __init__(self, master=None, size=40, target_class=None, is_z = False, printer_class=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        
        self.target_class = target_class
        self.printer_class = printer_class
        self.is_z = is_z
        self.canvas = tk.Canvas(self, width=size, height=size)
        self.canvas.create_polygon(7, 33, 20, 7, 33, 33, fill="black", outline="black")
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.pack()

    def on_click(self, event):
        
        if self.target_class.is_homed:
            if self.is_z:
                print("?Moving  "+str(self.target_class.xyz_step), " in Z-UP")
                self.target_class.move_xyz(x=0, y=0, z=self.target_class.xyz_step)
            else:
                print("?Moving  "+str(self.target_class.xyz_step), " in Y-UP")
                self.target_class.move_xyz(x=0, y=self.target_class.xyz_step, z=0)
        else:
            print("?? Printer not homed yet, please home the printer first")
            

class ArrowButtonLeft(tk.Frame):
    def __init__(self, master=None, size=40, target_class=None, printer_class=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        
        self.target_class = target_class
        self.printer_class = printer_class
        self.canvas = tk.Canvas(self, width=size, height=size)
        self.canvas.create_polygon(7, 20, 35, 7, 35, 33, fill="black", outline="black")
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.pack()

    def on_click(self, event):
        if self.target_class.is_homed:
            print("?Moving  "+str(self.target_class.xyz_step), " in X-DOWN")
            self.target_class.move_xyz(x=-self.target_class.xyz_step, y=0, z=0)
        else:
            print("?? Printer not homed yet, please home the printer first")


class ArrowButtonBottom(tk.Frame):
    def __init__(self, master=None, size=40, target_class=None, is_z = False, printer_class=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        self.target_class = target_class
        self.printer_class = printer_class
        self.is_z = is_z
        self.canvas = tk.Canvas(self, width=size, height=size)
        self.canvas.create_polygon(7, 7, 20, 33, 33, 7, fill="black", outline="black")
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.pack()

    def on_click(self, event):
        if self.target_class.is_homed:
            if self.is_z:
                print("?Moving  "+str(self.target_class.xyz_step), " in Z-DOWN")
                self.target_class.move_xyz(x=0, y=0, z=-self.target_class.xyz_step)
            else:
                print("?Moving  "+str(self.target_class.xyz_step), " in Y-DOWN")
                self.target_class.move_xyz(x=0, y=-self.target_class.xyz_step, z=0)
        else:
            print("?? Printer not homed yet, please home the printer first")
            

class RoundButton(tk.Canvas):
    def __init__(self, master=None, diameter=50, bg_color="lightgray", target_class=None, printer_class=None, **kwargs):
        tk.Canvas.__init__(self, master, width=diameter, height=diameter, bg=bg_color, highlightthickness=0, **kwargs)
        self.diameter = diameter

        self.target_class = target_class
        self.printer_class = printer_class
        # Draw a circle on the canvas
        radius = diameter // 2
        self.create_oval(0, 0, diameter, diameter, outline="black", fill=bg_color)

        self.bind("<Button-1>", self.on_click)

    def on_click(self, event):
        print("home position")
        self.printer_class.homing()
        # self.anycubic.set_home_pos(x=0, y=0, z=0)
        self.printer_class.max_x_feedrate(300)
        self.printer_class.max_y_feedrate(300)
        self.printer_class.max_z_feedrate(25)   
        self.printer_class.move_home()
        
        self.target_class.is_homed = True    
        [self.target_class.coord_value_text[i].set(0) for i in range(3)]
        [self.target_class.coord_value[i].configure(state='normal') for i in range(3)]
        
        
class MyWindow(ctk.CTk):
    def __init__(self): 
        super().__init__()
        # eventuellement ajouter des class pour les boutons, pour mieux gerer les scenarios, dui gnre les well plate button
        self.create_variables()
        self.isOpen = True
        
        self.title("X-Plant control panel")
        self.geometry("1200x750")
        self.protocol("WM_DELETE_WINDOW", self.close_window)

        self.title_ = ctk.CTkLabel(self, text="X-plant", font=("Arial Bold", 18))
        self.title_.grid(pady=10)

        self.gui_mode_frame = ctk.CTkFrame(self)
        self.gui_mode_frame.grid(row=2, column=0, padx=10, pady=15)
        self.gui_mode = ctk.CTkLabel(self.gui_mode_frame, text="GUI mode", font=("Arial Bold", 18))
        self.gui_mode.grid(row=0, column=0, padx=10, pady=10)
        self.gui_mode_menu = ctk.CTkOptionMenu(self.gui_mode_frame,
                                               values=["Light", "Dark", "System"],
                                               command=self.change_appearance_mode_event)
        self.gui_mode_menu.grid(row=0, column=1, padx=20, pady=(10, 0))
        self.gui_mode_menu.set(DEFAULT_MODE)
        
        self.tabControl = ctk.CTkTabview(self)

        for i in range(len(self.tabs_name)):
            self.tab.append(ctk.CTkFrame(self.tabControl))
            self.tabControl.add(self.tabs_name[i])
            self.set_tabs(i)
        self.tabControl.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")  # Adjust as needed
        self.columnconfigure(0, minsize=400, weight=1)
        self.rowconfigure(1, minsize=400,weight=1)
        
        
        self.tabControl.set(self.tabs_name[4])


    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)
    
    
    def create_variables(self):
        '''
        I created this because in some instance, I needed the variable to be created beforehand. At first, it was to make sure 
        I could delete something, even if it didn't exist, but it turns out I misused the winfo_exists() method.
        Before I realized this, I decided to pre create everything here, in order to avoid potential issues...
        Now, this also serves as a dictionnary of variables (somewhat incomplete, as I didn't properly update this function once
        I realized my mistake). But still, it is extremely useful. It's just that we can potentially remove half of the function
        and it would still work.
        '''
        self.is_homed = False
        self.load_parameters()
        self.tab        = []
        self.tabControl = None
        
        self.tabs_name      = ["Mode", "Cameras", "Parameters", "Well plate", 
                               "Motion Control", "Documentation"] 
        
        self.camera_displayed_text = tk.StringVar()
        self.displayed_cameras = 1
        self.camera_displayed_text.set("Camera "+str(self.displayed_cameras))
        self.frames         = [[],[]]
        self.camera_feed    = [[None, None, None],
                               [None]]
        self.camera_button_text = [None, None]
        self.create_well_variables()
        self.create_motion_variables()
        self.connect_printer_dynamixel()
        
    
    def load_parameters(self):
        with open(SETTINGS, 'r') as f:
            self.settings = json.load(f)
            
            
    def create_well_variables(self):
        # You can add any plates you want here, by defining the name in self.options and its layout in self.layout
        self.options        = ["TPP6", "TPP12", "TPP24", "TPP48", "NUNC48", "FALCON48"]
        self.label_col      = ["A", "B", "C", "D", "E", "F"]
        self.label_row      = ["1", "2", "3", "4", "5", "6", "7", "8"]
        self.layout         = [[2,3], # TPP6
                               [3,4], # TPP12
                               [4,6], # TPP24
                               [6,8], # TPP48
                               [6,8], # NUNC48
                               [6,8]] # FALCON48
        self.selected_wells = []
        self.well_dim_x     = 300
        self.well_dim_y     = 480
        self.well_menu           = None
        
        self.well_plate_grid    = None
        self.well_buttons       = []
        
        self.text_well_plate_explanation = ''' Here, you can select the well plate you want to use. It will display a simulation of the grid,
in which you can select UP TO 6 wells to use. You can then press the save button to save the selected wells into the config file.'''.replace('\n', ' ' )
        self.tab_well_explanation   = None    
        self.tab_well_results       = None
        self.text_well_results      = None
        self.remaining_wells        = None
        self.text_remaining_wells   = None
        self.well_button_grid       = None
        self.well_reset_button      = None
        self.well_save_button       = None
        
                
    def create_motion_variables(self):
        self.button_bottom  = None
        self.button_top     = None
        self.button_left    = None
        self.button_right   = None
                
        self.z_button_up    = None
        self.z_button_down  = None
        
        self.z_label = None                  
                
        self.offset = [0,0,0]
        
        self.safe_height        = 55
        self.xyz_grid_steps     = []
        self.xyz_step_buttons   = []
        self.xyz_step           = 0.1
        
        self.coord_value_grid   = None
        self.coord_label        = []
        self.coord_value        = []
        self.coord_value_text   = []
        
        self.servo_buttons      = []
        self.servo_frame        = []
        self.servo_labels       = []
        self.servo_values       = []
        self.servo_values_text  = []
        self.servo_gui_position = None
        self.unit_list          = ["steps", "percentage", "μl"]
        self.servo_unit_button  = None 
        self.is_unit_percentage = False
        self.servo_step_buttons = []
        self.servo_grid_steps   = None
        self.servo_step         = 1
        self.servo_pos          = []
        
        self.servo_names        = ["Servo pipette 1", "Servo pipette 2", "Servo speed"]
        self.toolhead_position  = ["Neutral", "Tip one", "Tip two"]
        
        
        self.tip_number     = 0
        self.pipette_empty  = 575 ## this variable shouldn't exists! We should calibrate with the value inside write_pipette_ul
        self.pipette_max_ul = self.pipette_empty+100 # ONLY FOR PURGING
        self.servo_pos      = [self.pipette_empty, self.pipette_empty, 30]
        
        self.buffer_moves = []
                
                
    def connect_printer_dynamixel(self):
        self.anycubic = Printer(descriptive_device_name="printer", 
                                port_name=get_com_port("1A86", "7523"), 
                                baudrate=115200)
        
        self.dynamixel = Dynamixel(ID=[1,2,3], 
                                   descriptive_device_name="XL430 test motor", 
                                   series_name=["xl", "xl", "xl"], 
                                   baudrate=57600,
                                   pipette_max_ul = self.pipette_max_ul,
                                   port_name=get_com_port("0403", "6014"))
        
        self.anycubic.connect()
        if debug == False:
            self.anycubic.change_idle_time(time = 300)
        
        self.dynamixel.begin_communication()
        self.dynamixel.set_operating_mode("position", ID="all")
        self.dynamixel.write_profile_velocity(100, ID="all")
        self.dynamixel.set_position_gains(P_gain = 2700, I_gain = 50, D_gain = 5000, ID=1)
        self.dynamixel.set_position_gains(P_gain = 2700, I_gain = 90, D_gain = 5000, ID=2)
        self.dynamixel.set_position_gains(P_gain = 2500, I_gain = 40, D_gain = 5000, ID=3)
        self.dynamixel.select_tip(tip_number=self.tip_number, ID=3)
        self.dynamixel.write_pipette_ul(self.pipette_empty, ID=[1,2])
        self.dynamixel.write_profile_velocity(self.servo_pos[-1], ID=[1,2])
        
        self.purging = False
        
            
    def set_tabs(self, i): # maybe there's a cleaner way of doing this
        if i == self.tabs_name.index("Mode"):
            self.set_tab_mode()
        elif i == self.tabs_name.index("Cameras"):
            self.set_tab_cameras()
        elif i == self.tabs_name.index("Parameters"):
            self.set_tab_parameters()
        elif i == self.tabs_name.index("Well plate"):
            self.set_tab_well_plate()
        elif i == self.tabs_name.index("Motion Control"):
            self.set_tab_motion_control()
        elif i == self.tabs_name.index("Documentation"):
            self.set_tab_documentation()
            
                  
    def debug(self):
        print("test")
        
    
    #### Functions related to the mode tab ####            
    def set_tab_mode(self):
        
        self.mode_camera_button = ctk.CTkButton(self.tabControl.tab("Mode"), 
                                             textvariable=self.camera_displayed_text,
                                             command= self.show_camera_control)
        self.mode_camera_button.grid(row=0)
        #### CHANGE TO CTK, FIND HOW TO MAKE IT CLEAN AND WORK
        self.camera_feed_mode = tk.Label(self.tabControl.tab("Mode"), width=480, height=270)
        self.camera_feed_mode.grid(row=1)  
        
    
    #### Functions related to the camera tab ####
    def set_tab_cameras(self):
        
        ## find how to increase image size according to label size
        self.camera_feed_camera_0 = tk.Label(self.tabControl.tab("Cameras"), width=640, height=360)
        self.camera_feed_camera_0.place(relx=0.1, rely=0.2)
        self.camera_feed_camera_1 = tk.Label(self.tabControl.tab("Cameras"), width=640, height=360)
        self.camera_feed_camera_1.place(relx=0.6, rely=0.2)
        
        if debug == False:
            self.stream1 = cam_gear.camThread("Camera 1", get_cam_index("TV Camera")) 
            self.stream1.start()
            frame = cam_gear.get_cam_frame(self.stream1)  
            self.cam = cv.Camera(frame)
            self.frame = self.cam.undistort(frame)
            self.invert = cv.invert(self.frame)
            self.mask = cv.create_mask(200, self.frame.shape[0:2], (self.frame.shape[1]//2, self.frame.shape[0]//2))
            self.intruder_detector = cv.create_intruder_detector()
            self.min_radius = 15
            self.max_radius = 38
            self.detect_attempt = 0
            self.max_detect_attempt = 50
            
            # Camera 2 - Macro Camera
            self.stream2 = cam_gear.camThread("Camera 2", get_cam_index("USB2.0 UVC PC Camera"))
        else:
            self.stream1 = cv2.imread("Developpement/captured_image.jpg")
            self.stream2 = cam_gear.camThread("Camera 2", 0) # laptop camera
        self.stream2.start()
        self.macro_frame = cam_gear.get_cam_frame(self.stream2)
        self.picture_pos = -self.settings["Offset"]["Tip one"][0]
        
        
    def update_cameras(self):
        ### change this, we don't need to undistort everytime i think
        ## We capture the frame and format it accordingly to be used by tkinter, 
        if debug == False:
            frame = cam_gear.get_cam_frame(self.stream1) 
            self.frame = self.cam.undistort(frame)
            self.invert = cv.invert(self.frame)  ### a quoi sert ce invert ??
            img = self.frame.copy()
            self.format_image(img, idx = 0)
        else:
            frame = cv2.imread("Developpement/captured_image.jpg")
            self.format_image(frame, idx = 0)    
        self.macro_frame = cam_gear.get_cam_frame(self.stream2) 
        self.format_image(self.macro_frame, idx = 1)
        self.display_camera_feed()
        
        
    def format_image(self, img, idx):
        img = cv2.resize(img, (320, 180))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        self.frames[idx] = ImageTk.PhotoImage(image=img)
        
        
    def display_camera_feed(self):
        ## make this look nicer please
        self.camera_feed_mode.configure(image=self.frames[self.displayed_cameras-1])
        self.camera_feed_mode.image = self.frames[self.displayed_cameras-1]
        self.camera_feed_control.configure(image=self.frames[self.displayed_cameras-1])
        self.camera_feed_control.image = self.frames[self.displayed_cameras-1]
        
        self.camera_feed_camera_0.configure(image=self.frames[0])
        self.camera_feed_camera_0.image = self.frames[0]
        self.camera_feed_camera_1.configure(image=self.frames[1])
        self.camera_feed_camera_1.image = self.frames[1]
        
        
    #### Functions related to the parameter tab ####    
    def set_tab_parameters(self):
        tab_index = self.tabControl.tab("Parameters")
        
        self.update_parameters()
        
        self.edit_parameter_frame = ctk.CTkFrame(tab_index)
        self.edit_parameter_frame.place(relx = 0.6, rely=0.3)
        
        self.param_list = list(self.settings.keys())
        self.param_list.remove("Well")
        self.param_list.remove("Saved Positions")
        
        self.clicked_parameter_1 = ctk.StringVar()
        self.clicked_parameter_1.set(self.param_list[0])
        self.parameter_menu = ctk.CTkOptionMenu(self.edit_parameter_frame,
                                                variable=self.clicked_parameter_1,
                                                values = self.param_list,
                                                command=self.show_parameters)
        self.parameter_menu.grid(column=0, row=0, sticky="w")
        self.show_parameters(self.clicked_parameter_1.get())  ## maybe there's a way to not call this
        self.empty_label_param_1 = ctk.CTkLabel(self.edit_parameter_frame, text=" ").grid(column=0, row=1, sticky="w")
        
    
    def show_parameters(self, click):
        try:
            self.sub_parameter_frame.grid_forget()
        except:
            pass
        self.sub_parameter_frame = ctk.CTkFrame(self.edit_parameter_frame, fg_color="transparent")
        self.sub_parameter_frame.grid(column=0, row=2, sticky="w")
        self.clicked_parameter_2 = ctk.StringVar()
        self.parameter_menu_2 = ctk.CTkOptionMenu(self.sub_parameter_frame,
                                                  variable=self.clicked_parameter_2,
                                                  values=list(self.settings[click].keys()))
        self.clicked_parameter_2.set(list(self.settings[click].keys())[0])
        self.parameter_menu_2.grid(column=0, row=0, sticky="w")
        
        self.empty_label_param_2 = ctk.CTkLabel(self.sub_parameter_frame, text=" ").grid(column=0, row=1, sticky="w")
        
        if type(list(self.settings[self.clicked_parameter_1.get()].values())[0]) == list: 
            self.entry_param_xyz = ctk.CTkFrame(self.sub_parameter_frame)
            self.entry_param_xyz.grid(column=0, row=2)
            self.entry_param_xyz_list = []
            self.entry_param_xyz_label = []
            for i in range(3):
                self.entry_param_xyz_label.append(ctk.CTkLabel(self.entry_param_xyz, text="X" if i==0 else "Y" if i==1 else "Z"))
                self.entry_param_xyz_label[i].grid(column=i, row=0, sticky="w", padx=5)
                self.entry_param_xyz_list.append(ctk.CTkEntry(self.entry_param_xyz, width=7))
                self.entry_param_xyz_list[i].grid(column=i, row=1, sticky="w", padx=5)
        else:
            self.entry_new_parameter = ctk.CTkEntry(self.sub_parameter_frame)
            self.entry_new_parameter.grid(column=0, row=3, sticky="w")
        
        self.empty_label_param_3 = ctk.CTkLabel(self.sub_parameter_frame, text=" ").grid(column=0, row=4, sticky="w")
        
        self.save_new_parameter_button = ctk.CTkButton(self.sub_parameter_frame, text="Save", command=self.save_new_parameter)
        self.save_new_parameter_button.grid(column=0, row=5, sticky="w")


    def save_new_parameter(self):
        
        param1 = self.clicked_parameter_1.get()
        param2 = self.clicked_parameter_2.get()
        if type(list(self.settings[param1].values())[0]) == list:
            temp_value = [None,None, None]
            for i in range(3):
                val = self.check_param_value(self.entry_param_xyz_list[i].get())
                if val == "Wrong value" :
                    return
                else:
                    temp_value[i] = val
            self.settings[param1][param2] = temp_value
        else:
            val = self.check_param_value(self.entry_new_parameter.get())
            if val == "Wrong value" :
                return
            else:
                self.settings[param1][param2] = val
        self.update_parameters()
   
   
    def check_param_value(self, val):
        val_return = True
        try:
            val_return = round(float(val), 2)
        except:
            print("Incorrect input. Please write a number here. If your number uses a comma, please replace it with '.'")
            return "Wrong value"    
        return val_return
    
    
    def update_parameters(self):
        try:
            self.parameter_frame.place_forget()
        except:
            pass
        # self.parameter_frame = tk.Frame(self.tabControl.tab("Parameters"))
        # self.parameter_frame.place(relx = 0.1, rely=0.1, relheight=0.8)
        
        self.parameter_treeview = ttk.Treeview(self.tabControl.tab("Parameters"), columns = ('Value',))
        self.parameter_treeview.heading('#0', text='Element')
        self.parameter_treeview.heading('Value', text='Value')
        
        self.populate_tree('', self.settings)
        self.parameter_treeview.place(relx = 0.1, rely=0.1, relheight=0.8, relwidth=0.34)
        
        # self.parameter_treeview.pack(expand=True, fill ='both')      
        
           
    def populate_tree(self, parent, dictionary):
        sub_name = ['X', 'Y', 'Z']
        for key, value in dictionary.items():
            if type(value) == dict:
                item = self.parameter_treeview.insert(parent, 'end', text=key, open=False)
                self.populate_tree(item, value)
         
            elif type(value) == list:
                item1 = self.parameter_treeview.insert(parent, 'end', text=key, open=True)
                for i in range(3):
                    item = self.parameter_treeview.insert(item1, 'end', text=sub_name[i], values=[str(value[i])])	
            else:
                item = self.parameter_treeview.insert(parent, 'end', text=key, values=[str(value)])
    
        
    #### Functions related to the Well plate tab ####    
    def set_tab_well_plate(self):
        # call menu function
        # call well plate function
        
        self.clicked_well = tk.StringVar()
        self.well_menu = ctk.CTkOptionMenu(self.tabControl.tab("Well plate"),
                                           variable=self.clicked_well,
                                           values=self.options,
                                           command=self.show_wells)    
             
        self.well_menu.place(relx=0.3, rely=0.3, anchor=tk.CENTER)
        
        self.well_menu_description = ctk.CTkLabel(self.tabControl.tab("Well plate"), text="Select a well plate")
        self.well_menu_description.place(relx=0.3, rely=0.2, anchor=tk.CENTER)
        
        self.tab_well_explanation = ctk.CTkLabel(self.tabControl.tab("Well plate"),  
                                             text=self.text_well_plate_explanation,
                                             width=100,
                                             wraplength=500) 
        self.tab_well_explanation.place(relx=0.3, rely=0.4, anchor=tk.CENTER)
        
        self.text_well_results = ctk.StringVar() # shows a list of selected wells
        self.tab_well_results = ctk.CTkLabel(self.tabControl.tab("Well plate"),
                                             textvariable=self.text_well_results,
                                             width=100,
                                             wraplength=500) 
        self.tab_well_results.place(relx=0.3, rely=0.5, anchor=tk.CENTER)
        
        self.text_remaining_wells = ctk.StringVar() # shows how many more wells you can still select
        self.remaining_wells = ctk.CTkLabel(self.tabControl.tab("Well plate"),
                                        textvariable=self.text_remaining_wells,
                                        width=100,
                                        wraplength=500)
        self.remaining_wells.place(relx=0.3, rely=0.55, anchor=tk.CENTER)
        
        
        self.well_button_grid = ctk.CTkFrame(self.tabControl.tab("Well plate"), width=300, height=480)
        
        self.well_button_grid.place(relx=0.3, rely=0.65, anchor=tk.CENTER)
        self.well_save_button = ctk.CTkButton(self.well_button_grid, 
                                           text="Save",
                                           command=self.save_well_settings)
        
        self.well_save_button.grid(column=0, row=0)
        self.well_reset_button = ctk.CTkButton(self.well_button_grid, 
                                            text="Reset", 
                                            command= lambda: self.show_wells(self.clicked_well.get())) 
        
        self.well_reset_button.grid(column=1, row=0)
    
            
    def show_wells(self, click):
        
        ## rewrite this to include a try except for place_forget()
        tab_index = self.tabControl.tab("Well plate")
        self.selected_well_plate = click
        if self.well_plate_grid is not None: # check if it exists
            self.well_plate_grid.place_forget()
            self.selected_wells = []
            self.text_well_results.set("")
            self.text_remaining_wells.set("")
            for i in range(len(self.well_buttons)): 
                self.well_buttons[i].grid_forget()
            self.well_buttons = []
            
            
        self.set_well_plate(self.well_dim_x, self.well_dim_y, well_id = self.options.index(click), tab_index=tab_index)
         

    def set_well_plate(self, well_dim_x, well_dim_y, well_id, tab_index):
        
        self.well_plate_grid = ctk.CTkFrame(tab_index, width=300, height=480, bg="lightgray")
        self.well_plate_grid.place(relx=0.7, rely=0.5, anchor=tk.CENTER)
        index = 0
        for i in range(self.layout[well_id][0]):
            self.well_plate_grid.grid_columnconfigure(i, minsize=well_dim_x/self.layout[well_id][0])
            for j in range(self.layout[well_id][1]):
                self.well_plate_grid.grid_rowconfigure(j, minsize=well_dim_y/self.layout[well_id][1])
                self.well_buttons.append(tk.Button(self.well_plate_grid, 
                                                   text=self.label_col[i]+self.label_row[j], 
                                                   width=5, 
                                                   relief="raised", 
                                                   command=lambda idx = index: (self.toggle_well(idx, self.layout[well_id]))))
                self.well_buttons[index].grid(column=i, row=j) 
                index = index + 1
                
    
    def toggle_well(self, index, layout):
        button = self.well_buttons[index]
        temp = self.label_row[index%layout[1]]
        temp2 = self.label_col[index//layout[1]]
        if button['relief'] == "sunken":
            button.configure(relief = "raised")
            self.selected_wells.remove(temp2+temp)
            if len(self.selected_wells)==0:
                self.text_well_results.set("")
            
        else:
            if (len(self.selected_wells) < 6):
                button.configure(relief = "sunken")
                self.selected_wells.append(temp2+temp)
        if len(self.selected_wells)>0:
            self.text_well_results.set("You have selected the following wells:"+str(self.selected_wells))
            
        if len(self.selected_wells)==6:
            self.text_remaining_wells.set("You cannot select more wells") 
            self.remaining_wells.configure(text_color="")
        else:
            self.text_remaining_wells.set("You can still select "+str(6-len(self.selected_wells))+" wells")
            self.remaining_wells.configure(text_color="black")
        
        
    def save_well_settings(self):
        self.settings["Well"]["Type"] = self.clicked_well.get()
        self.settings["Well"]["Number of well"] = len(self.selected_wells)
        for i in range(len(self.selected_wells)):
            self.settings["Well"][f"Culture {i+1}"] = self.selected_wells[i]    
        with open('TEST.json', 'w') as f:
            json.dump(self.settings, f, indent=4)
        self.update_parameters()

    
    #### Functions related to the motion control tab ####   
    def set_tab_motion_control(self):
        
        self.set_motor_control()
        self.set_servo_control()
        self.set_camera_for_control()


    def firmware_limit_overwrites(self):
        ## add a condition to make it work only when at x=0
        if self.firmware_limit_overwrites_text.get() == "Firmware limit overwrites : OFF":
            self.anycubic.set_position(-9)
            self.firmware_limit_overwrites_text.set("Firmware limit overwrites : ON")  
        else:
            self.anycubic.set_position(0)
            self.firmware_limit_overwrites_text.set("Firmware limit overwrites : OFF")
              
                              
    def set_motor_control(self):
        
        gui_x_pos = 0.15
        gui_y_pos = .5
        self.xyz_gui_position = ctk.CTkFrame(self.tabControl.tab("Motion Control"))
        self.xyz_gui_position.place(relx=gui_x_pos, rely=gui_y_pos, anchor=tk.CENTER)
        steps = [0.1, 1, 5, 10, 25, 50]
        coords_name = ["X", "Y", "Z"]
        
        self.set_toolhead_menus(gui_x_pos)
        
        ### TODO     ALREADY APPLY OFFSET IF PRINTER IS HOMED TODO
        
        self.button_right = ArrowButtonRight(self.xyz_gui_position, target_class=self, printer_class=self.anycubic)
        self.button_right.grid(column=2, row=2, padx=10, pady=10)
        
        self.button_left = ArrowButtonLeft(self.xyz_gui_position, target_class=self, printer_class=self.anycubic)
        self.button_left.grid(column=0, row=2, padx=10, pady=10)
        
        self.button_top = ArrowButtonTop(self.xyz_gui_position, target_class=self, printer_class=self.anycubic)
        self.button_top.grid(column=1, row=1, padx=10, pady=10)
        
        self.button_bottom = ArrowButtonBottom(self.xyz_gui_position, target_class = self, printer_class=self.anycubic)
        self.button_bottom.grid(column=1, row=3, padx=10, pady=10)
        
        self.center_button = RoundButton(self.xyz_gui_position, diameter=50, bg_color="black", target_class=self, printer_class=self.anycubic)
        self.center_button.grid(column=1, row=2, padx=10, pady=10)
        self.z_button_up = ArrowButtonTop(self.xyz_gui_position, is_z=True, target_class = self, printer_class=self.anycubic)
        self.z_button_up.grid(column=3, row=1, padx=10, pady=10)
        
        self.z_button_down = ArrowButtonBottom(self.xyz_gui_position, is_z=True, target_class = self, printer_class=self.anycubic)
        self.z_button_down.grid(column=3, row=3, padx=10, pady=10)
        
        
        self.z_label = ctk.CTkLabel(self.xyz_gui_position, text=coords_name[2])
        self.z_label.grid(column=3, row=2, padx=10, pady=10)                      
        
        self.xyz_grid_steps = ctk.CTkFrame(self.tabControl.tab("Motion Control"))
        self.xyz_grid_steps.place(relx=gui_x_pos+0.015, rely=gui_y_pos-.23, anchor=tk.CENTER)
        
        for i in range(3): 
            self.xyz_step_buttons.append(tk.Button(self.xyz_grid_steps, 
                                                text=str(steps[2*i]), 
                                                width=5, 
                                                command = lambda step = steps[2*i], idx = 2*i: self.toggle_step(step, idx, 'xyz')))
            self.xyz_step_buttons[2*i].grid(column=0+2*i, row=0)
            if i==0:
                self.xyz_step_buttons[i].configure(relief = "sunken")
            self.xyz_step_buttons.append(tk.Button(self.xyz_grid_steps, 
                                                text=str(steps[2*i+1]), 
                                                width=5, 
                                                command = lambda step = steps[2*i+1], idx = 2*i+1, : self.toggle_step(step,idx, 'xyz'))) ### set command here
            self.xyz_step_buttons[2*i+1].grid(column=1+2*i, row=0)
        
        
        ####
        self.coord_value_grid = ctk.CTkFrame(self.tabControl.tab("Motion Control"))
        self.coord_value_grid.place(relx=gui_x_pos+0.015, rely= gui_y_pos+0.35, anchor=tk.CENTER)
        
        for i in range(len(coords_name)):
            self.coord_label.append(ctk.CTkLabel(self.coord_value_grid, text=coords_name[i])) 
            self.coord_label[i].grid(column=i, row=5, padx=17, pady=10)
            
            self.coord_value_text.append(ctk.StringVar())
            self.coord_value.append(ctk.CTkEntry(self.coord_value_grid, 
                                             width=7, 
                                             textvariable=self.coord_value_text[i],
                                             state='readonly'))  
            self.coord_value[i].grid(column=i, row=6, padx=17, pady=10)
        
        self.move_xyz_button = ctk.CTkButton(self.coord_value_grid, text="Move", command=lambda: self.move_xyz(move_button_cmd=True))
        self.move_xyz_button.grid(column=0, row=7, pady=15)   
        
        self.reset_axis_button = ctk.CTkButton(self.coord_value_grid, text="Reset axis", command=self.reset_axis)
        self.reset_axis_button.grid(column=2, row=7, pady=15)
    
    def set_toolhead_menus(self, gui_x_pos):
       
        self.pipette_selector_frame = ctk.CTkFrame(self.tabControl.tab("Motion Control"))
        self.pipette_selector_frame.place(relx=gui_x_pos+0.015, rely=0.07, anchor=tk.CENTER)
        self.pipette_name = list(self.settings.get("Offset").keys())[1:]
        
        self.offset_selector_text = ctk.CTkLabel(self.pipette_selector_frame, text="Toolhead's offset")
        self.offset_selector_text.grid(column=0, row=0, padx=10, pady=5)
        
        self.clicked_offset = ctk.StringVar()
        self.pipette_offset_selector = ctk.CTkOptionMenu(self.pipette_selector_frame,
                                                         variable=self.clicked_offset,
                                                         values=self.pipette_name,
                                                         command=self.select_offset)
        self.clicked_offset.set(self.pipette_name[0])
        self.pipette_offset_selector.grid(column=0, row=1)

        self.pipette_selector_text = ctk.CTkLabel(self.pipette_selector_frame, text="Toolhead's servo's position")
        self.pipette_selector_text.grid(column=1, row=0, padx=10, pady=5)
        
        self.clicked_pipette = ctk.StringVar()
        self.pipette_selector = ctk.CTkOptionMenu(self.pipette_selector_frame,
                                                  variable=self.clicked_pipette,
                                                  values=self.toolhead_position,
                                                  command=self.select_tip)
        self.clicked_pipette.set(self.toolhead_position[0])
        self.pipette_selector.grid(column=1, row = 1) 
        
    
    def select_tip(self, value):
        # make it so it also changes the offset maybe, both internally and visually(GUI)
        self.move_xyz(go_safe_height=True) 
        
        self.dynamixel.select_tip(tip_number=self.toolhead_position.index(value), ID=3)     
        
        
    def select_offset(self, value):
        self.offset = self.settings["Offset"][value]  
        ### ajouter un wait peut etre pour pas qu'il le fasse en même temps
        self.move_xyz(go_safe_height=True) 
        
    
    def move_xyz(self, x=0, y=0, z=0, move_button_cmd=False, go_safe_height = False):
        ## maybe add a drop down menu with a list of every known position as to make everything faster
        ## maybe add a drop down menu setting the speeds !
        for i in range(len(self.coord_value_text)):
            if move_button_cmd:
                try:
                    float(self.coord_value_text[i].get())
                except:
                    print("You need to enter XYZ coords as value, with '.', not letters or other symbols")
                    return
        if move_button_cmd or go_safe_height:
            x = round(float(self.coord_value_text[0].get()),2)
            y = round(float(self.coord_value_text[1].get()),2)
            z = round(float(self.coord_value_text[2].get()),2)
        else:
            x = round(float(self.coord_value_text[0].get()) + x,2)
            y = round(float(self.coord_value_text[1].get()) + y,2)
            z = round(float(self.coord_value_text[2].get()) + z,2)
            
        if go_safe_height:
            z = self.safe_height
            
        if x < X_MIN:
            x = X_MIN
        elif x > X_MAX:
            x = X_MAX
        if y < Y_MIN:
            y = Y_MIN
        elif y > Y_MAX:
            y = Y_MAX
        if z < Z_MIN:
            z = Z_MIN
        elif z > Z_MAX:
            z = Z_MAX
            
        print("Setting position to X={}, Y={}, Z={}".format(x,y,z))
        print("Offset is {}".format(self.offset))
        self.anycubic.move_axis_relative(x=x, y=y, z=z, offset=self.offset)
        self.coord_value_text[0].set(str(x))
        self.coord_value_text[1].set(str(y))
        self.coord_value_text[2].set(str(z))
        # Maybe find a way to read the coordinate instead of writing them manually into self.coord_value_text  
        
    
    def reset_axis(self):
        self.anycubic.disable_axis(all=True)
        self.offset = [0,0,0]
        self.clicked_offset.set(self.pipette_name[0])
        for i in range(3):
            self.coord_value_text[i].set("")
            self.coord_value[i].configure(state='readonly')
        self.is_homed = False
        
                
    def set_servo_control(self):

        gui_x_pos = 0.85
        gui_y_pos = 0.5
        spacing = 20
        steps = [1, 5, 10, 25, 50, 100]
        
        button_height = 8
        # self.servo_unit_text = tk.StringVar()
        # self.servo_unit_text.set("Unit currently set to : steps")
        # self.is_unit_percentage = False
        
        self.servo_gui_position = ttk.Frame(self.tabControl.tab("Motion Control"))
        self.servo_gui_position.place(relx=gui_x_pos, rely=gui_y_pos, anchor=tk.CENTER)
        
        # self.servo_unit_button = ttk.Button(self.tabControl.tab("Motion Control"), 
        #                                     textvariable=self.servo_unit_text, 
        #                                     command=self.change_unit_servo)
        # self.servo_unit_button.place(relx=gui_x_pos-0.033, rely=0.15, anchor=tk.CENTER)
        
        self.clicked_servo_unit = tk.StringVar()
        self.clicked_servo_unit.set(self.unit_list[0])
        self.servo_unit_list_menu = tk.OptionMenu(self.tabControl.tab("Motion Control"),
                                                  self.clicked_servo_unit,
                                                  *self.unit_list,
                                                  command=self.change_unit_servo)
        self.servo_unit_list_menu.place(relx=gui_x_pos-0.033, rely=0.15, anchor=tk.CENTER)
        text = ["Eject", "Pump"]
        
        for i in range(len(self.servo_names)):
            if i == 2:
                text = ["+", "-"]
            self.servo_frame.append(ttk.Frame(self.servo_gui_position))
            self.servo_frame[i].grid(column=i, row=0, ipadx=spacing)
            
            self.servo_labels.append(tk.Label(self.servo_frame[i], text=self.servo_names[i]))
            self.servo_labels[i].grid(column=0, row=0, pady = 10)
            self.servo_buttons.append(ttk.Button(self.servo_frame[i], 
                                                 text=text[0], 
                                                 width=4,
                                                 command = lambda idx = i: self.move_servo('+', idx)))
            self.servo_buttons[2*i].grid(column=0, row=1, ipady=button_height)
            
            self.servo_buttons.append(ttk.Button(self.servo_frame[i], 
                                                 text=text[1], 
                                                 width=4,
                                                 command = lambda idx = i: self.move_servo('-', idx)))
            self.servo_buttons[2*i+1].grid(column=0, row=2, ipady=button_height)
            
            self.servo_values_text.append(tk.StringVar())
            self.servo_values_text[i].set(self.servo_pos[i])
            self.servo_values.append(tk.Label(self.servo_frame[i], textvariable=self.servo_values_text[i]))
            self.servo_values[i].grid(column=0, row=5, pady = 15)
            
        #### Buttons for deciding the values of the steps
        self.servo_grid_steps = ttk.Frame(self.tabControl.tab("Motion Control"))
        self.servo_grid_steps.place(relx=gui_x_pos-0.03, rely=gui_y_pos-.23, anchor=tk.CENTER)
        
        for i in range(3): 
            self.servo_step_buttons.append(tk.Button(self.servo_grid_steps, 
                                                text=str(steps[2*i]), 
                                                width=5, 
                                                command = lambda step = steps[2*i], idx = 2*i: self.toggle_step(step, idx, 'servo')))
            self.servo_step_buttons[2*i].grid(column=0+2*i, row=0)
            
            if i == 0:
                self.servo_step_buttons[i].configure(relief = "sunken")
            self.servo_step_buttons.append(tk.Button(self.servo_grid_steps, 
                                                text=str(steps[2*i+1]), 
                                                width=5, 
                                                command = lambda step = steps[2*i+1], idx = 2*i+1, : self.toggle_step(step,idx, 'servo'))) ### set command here
            self.servo_step_buttons[2*i+1].grid(column=1+2*i, row=0)
        
        #### Buttons for saving the positions of the servos and the motors
        self.save_position_gui = ttk.Frame(self.tabControl.tab("Motion Control"))
        self.save_position_gui.place(relx=gui_x_pos-0.03, rely=gui_y_pos+0.3, anchor=tk.CENTER)   
        
        self.save_text = tk.Label(self.save_position_gui, text=f'''You can save the current positions of the motor and the servo.  \n They will be saved in the {SETTINGS} as : ''')
        self.save_text.grid(column=0, row=1)
        
        self.empty_label1 = tk.Label(self.save_position_gui, text=" ")
        self.empty_label1.grid(column=0, row=2)
        self.empty_label1.rowconfigure(1, minsize=2, weight=1)
        
        self.save_name_entry = tk.Entry(self.save_position_gui, width=15)
        self.save_name_entry.grid(column=0, row=3)
        self.empty_label2 = tk.Label(self.save_position_gui, text=" ")
        self.empty_label2.grid(column=0, row=4)
        self.empty_label2.rowconfigure(3, minsize=2, weight=1)
        self.save_pos_button = ttk.Button(self.save_position_gui, text="Save", command=self.save_pos)
        self.save_pos_button.grid(column=0, row=5)
        
        self.purge_button_text = tk.StringVar()
        self.purge_button_text.set("Purging OFF")
        self.purge_button = ttk.Button(self.save_position_gui, 
                                       textvariable=self.purge_button_text, 
                                       command=self.purge)
        self.purge_button.grid(column=0, row=0)
     
     
    def purge(self):
        ### MAKE SURE THIS HAPPENS ONLY AT 0: OR SOME SORT OF SECURITY
         if self.purge_button_text.get() == "Purging OFF":
             self.purge_button_text.set("Purging ON")
             self.purging = True
         else:
            self.purge_button_text.set("Purging OFF")
            self.purging = False
         
         
    def move_servo(self, sign, idx):
        
        ## add something for the purge here
        if not(self.clicked_servo_unit.get() == self.unit_list[1]) or idx == 2:
            delta = self.servo_step*(1 if sign == '+' else -1)
        else:
            delta = self.servo_step*(1 if sign == '+' else -1)*self.pipette_empty/100
            
        self.servo_pos[idx] = round(self.servo_pos[idx] + delta,1)
            
        if idx == 2:
            if self.servo_pos[idx] > 100:
                self.servo_pos[idx] = 100
            elif self.servo_pos[idx] < 0:
                self.servo_pos[idx] = 0
            self.dynamixel.write_profile_velocity(self.servo_pos[idx], ID=[1,2])
            self.servo_values_text[idx].set(self.servo_pos[idx])
        else:
            if self.servo_pos[idx] > self.pipette_empty and self.purging == False:
                self.servo_pos[idx] = self.pipette_empty
            elif self.servo_pos[idx] > self.pipette_max_ul and self.purging == True:
                self.servo_pos[idx] = self.pipette_max_ul
            elif self.servo_pos[idx] < 0:
                self.servo_pos[idx] = 0
                
            self.dynamixel.write_pipette_ul(volume_ul=self.servo_pos[idx], ID=idx+1, purging = self.purging)
            self.display_servo_pos()
        
        
    def set_camera_for_control(self):
        self.camera_control_frame = tk.Frame(self.tabControl.tab("Motion Control"))
        self.camera_control_frame.place(relx=0.5, rely=0.3, anchor=tk.CENTER)  
           
        self.control_camera_button = ttk.Button(self.camera_control_frame, 
                                                textvariable=self.camera_displayed_text, 
                                                command=self.show_camera_control)
        self.control_camera_button.pack()
        
        self.camera_feed_control = tk.Label(self.camera_control_frame, width=480, height=270)
        self.camera_feed_control.pack()
    
    
    def show_camera_control(self): 
        if self.camera_displayed_text.get() == "Camera 1":
            self.camera_displayed_text.set("Camera 2")
            self.displayed_cameras = 2
        else:
            self.camera_displayed_text.set("Camera 1")
            self.displayed_cameras = 1
    
        
    def change_unit_servo(self, value):
        # self.clicked_servo_unit.set(value)
        # if not(self.is_unit_percentage):
        #     self.clicked_servo_unit.set("Unit currently set to : percentage")
        #     self.is_unit_percentage = True
        # else:
        #     self.clicked_servo_unit.set("Unit currently set to : steps")
        #     self.is_unit_percentage = False
        self.display_servo_pos()
            
    
    def display_servo_pos(self):
        
        if self.clicked_servo_unit.get() == self.unit_list[1]:
            self.servo_values_text[0].set(str(round(self.servo_pos[0]/self.pipette_empty*100,1))+"%")
            self.servo_values_text[1].set(str(round(self.servo_pos[1]/self.pipette_empty*100,1))+"%")   
        elif self.clicked_servo_unit.get() == self.unit_list[2]:
            self.servo_values_text[0].set(str(round(self.pipette_empty-self.servo_pos[0],1))+"μl")
            self.servo_values_text[1].set(str(round(self.pipette_empty-self.servo_pos[1],1))+"μl")   
        else:
            self.servo_values_text[0].set(str(self.servo_pos[0]))
            self.servo_values_text[1].set(str(self.servo_pos[1]))
            
            
    def toggle_step(self, step, idx, type):
        if type == 'xyz':
            self.xyz_step = step 
            button_list = self.xyz_step_buttons
        elif type == 'servo':
            self.servo_step = step 
            button_list = self.servo_step_buttons
        else:
            print("error when defining type of buttons for steps")
        for i in range(len(button_list)):
            if i == idx:
                button_list[i].configure(relief = "sunken")
            else:
                button_list[i].configure(relief = "raised")
            
    
    def save_pos(self):
        if self.settings.get('Saved Positions') == None:
            self.settings['Saved Positions'] = {}
        var = self.save_name_entry.get()
        self.settings['Saved Positions'][var] = {}
        self.settings['Saved Positions'][var]["X"] = self.coord_value_text[0].get()
        self.settings['Saved Positions'][var]["Y"] = self.coord_value_text[1].get()
        self.settings['Saved Positions'][var]["Z"] = self.coord_value_text[2].get()
        self.settings['Saved Positions'][var]["Servo 1"] = self.servo_pos[0]
        self.settings['Saved Positions'][var]["Servo 2"] = self.servo_pos[1]
        self.settings['Saved Positions'][var]["Servo Speed"] = self.servo_pos[2] 
        self.update_parameters()
            
    def add_function_to_buffer(self, function, *args):
        # add a function to the buffer
        # function is the function to be executed
        # *args are the arguments of the function
        self.buffer_moves.append([function, args])
        
        
    def execute_function_from_buffer(self):
        # check if current move is done
        # if yes, removes first entry from buffer and executes it
        # if no, return
        # if move is done:
        #     self.buffer_moves.pop(0)
        #     self.buffer_moves[0][0](*self.buffer_moves[0][1]) ## maybe remove star
        pass
        
        
    def set_tab_documentation(self):
        # self.documentation_frame = tk.Frame(self.tab[self.tabs_name.index("Documentation")])
        self.documentation_frame = tk.Frame(self.tabControl.tab("Documentation"))
        self.documentation_frame.pack(expand=True, fill ='both')
        
        self.doc_text = tk.Text(self.documentation_frame, width=100, height=100)
        self.doc_text.pack(expand=True, fill ='both')
        self.documentation_text = '''test, test
        test'''
        self.doc_text.insert(tk.END, self.documentation_text)
        self.doc_text.configure(state='disabled')
        self.doc_text.configure(relief="flat")
     
               
    def close_window(self):  
        with open("TEST.json", "w") as jsonFile:
            json.dump(self.settings, jsonFile, indent=4)
        try :
            self.stream2.stop()
        except:
            pass
        try:
            self.stream1.stop()
        except:
            pass
        self.destroy()
        self.isOpen = False
        

if __name__ == "__main__":
    window = MyWindow()
    
    while window.isOpen:
        window.update_cameras()
        window.execute_function_from_buffer()
        # maybe create a liste of coordinate, that is the waitlist for the commands, and then execute them one by one, once the one prior is done ?
        # check how the code handles 2 xyz moves commands in a row, maybe it's just between the anycubic and the dynamixel that there is no wait time
        window.update()
        window.update_idletasks()

