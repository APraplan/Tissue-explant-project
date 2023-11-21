import tkinter as tk                     
from tkinter import ttk 
import json

import sys

sys.path.append('Platform')
sys.path.append('Pictures')
sys.path.append('Communication')
    
from Communication.ports_gestion import *
import Platform.computer_vision as cv
from PIL import Image, ImageTk
import Developpement.Cam_gear as cam_gear
import cv2

debug = True

if debug:
    from Communication.fake_communication import * 
else:
    from Communication.dynamixel_controller import *
    from Communication.printer_communications import * 
    import Developpement.Cam_gear as cam_gear
    

### ATTENTION AU OFFSET  !!!

SETTINGS = "TEST.json"
X_MIN = 0.0
X_MAX = 220.0
Y_MIN = 0.0
Y_MAX = 220.0
Z_MIN = 0.0
Z_MAX = 220.0

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
        
        
class MyWindow(tk.Tk):
    def __init__(self): 
        super().__init__()
        # eventuellement ajouter des class pour les boutons, pour mieux gerer les scenarios, dui gnre les well plate button
        self.create_variables()
        self.isOpen = True
        
        self.title("X-Plant control panel")
        self.geometry("1200x700")
        self.protocol("WM_DELETE_WINDOW", self.close_window)

        self.title_ = tk.Label(self, text="X-plant", font=("Arial Bold", 18))
        self.title_.grid()

        # Create a style to configure the notebook
        self.style = ttk.Style()
        self.style.configure("TNotebook.Tab", padding=(15, 10))  # Adjust the padding values as needed
        
        self.style.configure('cameraStyle.TFrame', background="black")  

        self.tabControl = ttk.Notebook(self)

        for i in range(len(self.tabs_name)):
            self.tab.append(ttk.Frame(self.tabControl))
            self.tabControl.add(self.tab[i], text=self.tabs_name[i])
            self.set_tabs(i)
        self.tabControl.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")  # Adjust as needed
        self.columnconfigure(0, minsize=400, weight=1)
        self.rowconfigure(1, minsize=400,weight=1)

        
        
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
        self.style      = None
        self.tabControl = None
        
        self.tabs_name      = ["Cameras", "Mode", "Parameters", "Well plate", 
                               "Motion Control", "Documentation"] # Change the orders of the tabs, good for debugging
        
        self.camera_displayed_text = tk.StringVar()
        self.camera_displayed_text.set("Camera 2")
        self.frames         = [[],[]]
        self.camera_feed    = [[None, None, None],
                            [None]]
        self.displayed_cameras = 2
        self.camera_button_text = [None, None]
        self.create_well_variables()
        self.create_motion_variables()
        self.connect_printer_dynamixel()
        
    
    def load_parameters(self):
        with open(SETTINGS, 'r') as f:
            self.settings = json.load(f)
            
            
    def create_well_variables(self):
        self.options        = ["TPP6", "TPP12", "TPP24", "TPP48", "NUNC48", "FALCON48"]
        self.label_col      = ["A", "B", "C", "D", "E", "F"]
        self.label_row      = ["1", "2", "3", "4", "5", "6", "7", "8"]
        self.layout         = [[2,3], [3,4], [4,6], [6,8], [6,8], [6,8]]
        self.selected_wells = []
        self.well_dim_x     = 300
        self.well_dim_y     = 480
        self.well_menu           = None
        
        self.well_plate_label   = None
        self.well_plate         = None
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
        
        self.xyz_grid_steps     = []
        self.xyz_step_buttons   = []
        self.xyz_step           = 0.1
        
        self.coord_value_grid   = None
        self.coord_label = []
        self.coord_value = []
        self.coord_value_text = []
        
        self.servo_buttons      = []
        self.servo_frame        = []
        self.servo_labels       = []
        self.servo_values       = []
        self.servo_values_text  = []
        self.servo_gui_position = None
        self.servo_unit_button  = None 
        self.is_unit_percentage   = False
        self.servo_step_buttons = []
        self.servo_grid_steps   = None
        self.servo_step         = 1
        self.servo_pos          = []
        
        self.servo_names    = ["Servo pipette 1", "Servo pipette 2", "Servo speed"]
        
        self.tip_number = 0
        self.pipette_empty = 525
        self.servo_pos = [self.pipette_empty, self.pipette_empty, 30]
                
                
    def connect_printer_dynamixel(self):
        self.anycubic = Printer(descriptive_device_name="printer", 
                                port_name=get_com_port("1A86", "7523"), 
                                baudrate=115200)
        
        self.dynamixel = Dynamixel(ID=[1,2,3], 
                                   descriptive_device_name="XL430 test motor", 
                                   series_name=["xl", "xl", "xl"], 
                                   baudrate=57600,
                                   pipette_empty= 525, 
                                   port_name=get_com_port("0403", "6014"))
        
        self.anycubic.connect()
        
        self.dynamixel.begin_communication()
        self.dynamixel.set_operating_mode("position", ID="all")
        self.dynamixel.write_profile_velocity(100, ID="all")
        self.dynamixel.set_position_gains(P_gain = 2700, I_gain = 50, D_gain = 5000, ID=1)
        self.dynamixel.set_position_gains(P_gain = 2700, I_gain = 90, D_gain = 5000, ID=2)
        self.dynamixel.set_position_gains(P_gain = 2500, I_gain = 40, D_gain = 5000, ID=3)
        self.dynamixel.select_tip(tip_number=self.tip_number, ID=3)
        self.dynamixel.write_pipette_ul(self.pipette_empty, ID=[1,2])
        self.dynamixel.write_profile_velocity(self.servo_pos[-1], ID=[1,2])
        
            
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
            
                  
    def debug(self):
        print("test")
        
    
    #### Functions related to the mode tab ####            
    def set_tab_mode(self):
        tab_index = self.tabs_name.index("Mode")
        self.mode_camera_frame = tk.Frame(self.tab[tab_index])
        self.mode_camera_frame.pack()
        
        self.mode_camera_button = ttk.Button(self.mode_camera_frame, 
                                             textvariable=self.camera_displayed_text,
                                             command= self.show_camera_control)
        self.mode_camera_button.pack()
        self.camera_feed_mode = tk.Label(self.mode_camera_frame, width=480, height=270)
        self.camera_feed_mode.pack()  
        
    
    #### Functions related to the camera tab ####
    def set_tab_cameras(self):
        tab_index = self.tabs_name.index("Cameras")
        self.cameras_camera_frame = tk.Frame(self.tab[tab_index])
        self.cameras_camera_frame.pack()
        
        self.tesstLabel = tk.Label(self.cameras_camera_frame, text="test")
        self.tesstLabel.place(relx=0.1, rely=0.1)
        self.camera_feed_camera_0 = tk.Label(self.cameras_camera_frame, width=480, height=270)
        self.camera_feed_camera_0.place(relx=0.1, rely=0.1)
        self.camera_feed_camera_1 = tk.Label(self.cameras_camera_frame, width=480, height=270)
        self.camera_feed_camera_1.place(relx=0.5, rely=0.1)
        
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
        
        ## We capture the frame and format it accordingly to be used by tkinter, 
        if debug == False:
            frame = cam_gear.get_cam_frame(self.stream1) 
            self.frame = self.cam.undistort(frame)
            self.invert = cv.invert(self.frame)
            img = self.frame.copy()
            self.format_image(img, idx = 0)
        else:
            frame = cv2.imread("Developpement/captured_image.jpg")
            self.format_image(frame, idx = 0)    
        self.macro_frame = cam_gear.get_cam_frame(self.stream2) 
        self.format_image(self.macro_frame, idx = 1)
            
        
    def format_image(self, img, idx):
        img = cv2.resize(img, (320, 180))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        self.frames[idx] = ImageTk.PhotoImage(image=img)
        
        self.display_camera_feed()
        
        
    def display_camera_feed(self):
        ## make this look nicer please
        self.camera_feed_mode.configure(image=self.frames[self.displayed_cameras-1])
        self.camera_feed_mode.image = self.frames[self.displayed_cameras-1]
        self.camera_feed_control.configure(image=self.frames[self.displayed_cameras-1])
        self.camera_feed_control.image = self.frames[self.displayed_cameras-1]
        
        self.camera_feed_camera_0.configure(image=self.frames[0])
        self.camera_feed_camera_0.image = self.frames[0]
        # self.camera_feed_camera_1.configure(image=self.frames[1])
        # self.camera_feed_camera_1.image = self.frames[1]
        
        
    #### Functions related to the parameter tab ####    
    def set_tab_parameters(self):
        tab_index = self.tabs_name.index("Parameters")
        
        self.parameter_frame = tk.Frame(self.tab[tab_index])
        self.parameter_frame.place(relx = 0.1, rely=0.1, relheight=0.8)
        
        self.parameter_treeview = ttk.Treeview(self.parameter_frame, columns = ('Value',))
        self.parameter_treeview.heading('#0', text='Element')
        self.parameter_treeview.heading('Value', text='Value')
        
        self.populate_tree('', self.settings)
        self.parameter_treeview.pack(expand=True, fill ='both')
        
        
        self.edit_parameter_frame = tk.Frame(self.tab[tab_index])
        self.edit_parameter_frame.place(relx = 0.6, rely=0.3)
        
        self.param_list = list(self.settings.keys())
        self.param_list.remove("Well")
        
        self.parameter_clicked_1 = tk.StringVar()
        self.parameter_clicked_1.set(self.param_list[0])
        self.parameter_menu = ttk.OptionMenu(self.edit_parameter_frame,
                                             self.parameter_clicked_1,
                                             self.param_list[0],
                                             *self.param_list,
                                             command=self.show_parameters)
        self.parameter_menu.grid(column=0, row=0, sticky="w")
        self.show_parameters(self.parameter_clicked_1.get())
        self.empty_label_param_1 = tk.Label(self.edit_parameter_frame, text=" ").grid(column=0, row=1, sticky="w")
        
    
    def show_parameters(self, click):
        try:
            self.sub_parameter_frame.grid_forget()
        except:
            pass
        self.sub_parameter_frame = tk.Frame(self.edit_parameter_frame)
        self.sub_parameter_frame.grid(column=0, row=2, sticky="w")
        self.parameter_clicked_2 = tk.StringVar()
        self.parameter_clicked_2.set(" ")
        self.parameter_menu_2 = ttk.OptionMenu(self.sub_parameter_frame,
                                                self.parameter_clicked_2,
                                                list(self.settings[click].keys())[0],
                                                *list(self.settings[click].keys()))
        self.parameter_menu_2.grid(column=0, row=0, sticky="w")
        
        self.empty_label_param_2 = tk.Label(self.sub_parameter_frame, text=" ").grid(column=0, row=1, sticky="w")
        if type(list(self.settings[self.parameter_clicked_1.get()].values())[0]) == list: 
            self.entry_param_xyz = tk.Frame(self.sub_parameter_frame)
            self.entry_param_xyz.grid(column=0, row=2, sticky="w")
            self.entry_param_xyz_list = []
            self.entry_param_xyz_label = []
            for i in range(3):
                self.entry_param_xyz_label.append(tk.Label(self.entry_param_xyz, text="X" if i==0 else "Y" if i==1 else "Z"))
                self.entry_param_xyz_label[i].grid(column=i, row=0, sticky="w", padx=5)
                self.entry_param_xyz_list.append(tk.Entry(self.entry_param_xyz, width=7))
                self.entry_param_xyz_list[i].grid(column=i, row=1, sticky="w", padx=5)
        else:
            self.entry_new_parameter = tk.Entry(self.sub_parameter_frame)
            self.entry_new_parameter.grid(column=0, row=3, sticky="w")
        
        self.empty_label_param_3 = tk.Label(self.sub_parameter_frame, text=" ").grid(column=0, row=4, sticky="w")
        
        self.save_new_parameter_button = ttk.Button(self.sub_parameter_frame, text="Save", command=self.save_new_parameter)
        self.save_new_parameter_button.grid(column=0, row=5, sticky="w")


    def save_new_parameter(self):
        tab_index = self.tabs_name.index("Parameters")
        param1 = self.parameter_clicked_1.get()
        param2 = self.parameter_clicked_2.get()
        if type(list(self.settings[param1].values())[0]) == list:
            for i in range(3):
                if self.entry_param_xyz_list[i].get().isdigit():
                    self.settings[param1][param2][i] = round(float(self.entry_param_xyz_list[i].get()),2)
                elif self.entry_param_xyz_list[i].get() == "":
                    self.settings[param1][param2][i] = 0
                else:
                    print("Incorrect input. Please write a number here. If your number uses a comma, please replace it with '.'")
                    return
        else:
            if self.entry_new_parameter.get().isdigit():
                self.settings[param1][param2] = round(float(self.entry_new_parameter.get()),2) 
            elif self.entry_new_parameter.get() == "":
                return
            else:
                print("Incorrect input. Please write a number here. If your number uses a comma, please replace it with '.'")
                return
        self.parameter_frame.place_forget()
        self.parameter_frame = tk.Frame(self.tab[tab_index])
        self.parameter_frame.place(relx = 0.1, rely=0.1, relheight=0.8)
        
        self.parameter_treeview = ttk.Treeview(self.parameter_frame, columns = ('Value',))
        self.parameter_treeview.heading('#0', text='Element')
        self.parameter_treeview.heading('Value', text='Value')
        
        self.populate_tree('', self.settings)
        self.parameter_treeview.pack(expand=True, fill ='both')      
        
           
    def populate_tree(self, parent, dictionary):
        sub_name = ['X', 'Y', 'Z']
        for key, value in dictionary.items():
            if type(value) == dict:
                item = self.parameter_treeview.insert(parent, 'end', text=key, open=True)
                self.populate_tree(item, value)
         
            elif type(value) == list:
                item1 = self.parameter_treeview.insert(parent, 'end', text=key, open=True)
                for i in range(3):
                    item = self.parameter_treeview.insert(item1, 'end', text=sub_name[i], values=[str(value[i])])	
            else:
                item = self.parameter_treeview.insert(parent, 'end', text=key, values=[str(value)])
    
        
    #### Functions related to the Well plate tab ####    
    def set_tab_well_plate(self):
        
        tab_index = self.tabs_name.index("Well plate")
        
        self.clicked = tk.StringVar()
        self.clicked.set(" ")
        
        self.well_menu = ttk.OptionMenu(self.tab[tab_index], ## eventuellement changer pour un combobox.
                                  self.clicked,
                                  self.options[0],
                                  *self.options,
                                  command=self.show_wells)    
             
        # self.well_menu = ttk.Combobox(self.tab[tab_index], ## eventuellement changer pour un combobox.
        #                          state="readonly",
        #                          values=self.options,
        #                          command=self.show_wells) #look how to bind command to combobox
        self.well_menu.place(relx=0.3, rely=0.3, anchor=tk.CENTER)
        
        self.well_menu_description = tk.Label(self.tab[tab_index], text="Select a well plate")
        self.well_menu_description.place(relx=0.3, rely=0.2, anchor=tk.CENTER)
        
        self.tab_well_explanation = tk.Label(self.tab[tab_index],  
                                             text=self.text_well_plate_explanation,
                                             width=100,
                                             wraplength=500) 
        self.tab_well_explanation.place(relx=0.3, rely=0.4, anchor=tk.CENTER)
        
        self.text_well_results = tk.StringVar() # shows a list of selected wells
        self.tab_well_results = tk.Label(self.tab[tab_index],
                                             textvariable=self.text_well_results,
                                             width=100,
                                             wraplength=500) 
        self.tab_well_results.place(relx=0.3, rely=0.5, anchor=tk.CENTER)
        
        self.text_remaining_wells = tk.StringVar() # shows how many more wells you can still select
        self.remaining_wells = tk.Label(self.tab[tab_index],
                                             textvariable=self.text_remaining_wells,
                                             width=100,
                                             wraplength=500)
        self.remaining_wells.place(relx=0.3, rely=0.55, anchor=tk.CENTER)
        
        
        self.well_button_grid = tk.Frame(self.tab[tab_index], width=300, height=480)
        
        self.well_button_grid.place(relx=0.3, rely=0.65, anchor=tk.CENTER)
        self.well_save_button = ttk.Button(self.well_button_grid, 
                                           text="Save",
                                           command=self.save_well_settings)
        
        self.well_save_button.grid(column=0, row=0)
        self.well_reset_button = ttk.Button(self.well_button_grid, 
                                            text="Reset", 
                                            command= lambda: self.show_wells(self.clicked.get())) 
        
        self.well_reset_button.grid(column=1, row=0)
        # add the number of remaining cell one can select
        
        
    def show_wells(self, click):
        
        ## rewrite this to include a try except for place_forget()
        tab_index = self.tabs_name.index("Well plate")
        self.selected_well_plate = click
        if self.well_plate_label is not None: # check if it exists
            self.well_plate_label.place_forget()
            self.selected_wells = []
            self.text_well_results.set("")
            self.text_remaining_wells.set("")
            for i in range(len(self.well_buttons)): 
                self.well_buttons[i].grid_forget()
            self.well_buttons = []
            
        if self.well_plate is not None:
            self.well_plate.place_forget()
            
        self.set_well_plate(self.well_dim_x, self.well_dim_y, well_id = self.options.index(click), tab_index=tab_index)
         

    def set_well_plate(self, well_dim_x, well_dim_y, well_id, tab_index):
        
        self.well_plate_label = ttk.Label(self.tab[tab_index], text=self.clicked.get()) 
        self.well_plate_label.place(relx=0.7, rely=0.05, anchor=tk.CENTER)
        
        self.well_plate = tk.Frame(self.tab[tab_index], width=well_dim_x, height=well_dim_y, bg="lightgray") # make it look better, yikes
        self.well_plate.place(relx=0.7, rely=0.5, anchor=tk.CENTER)
        
        
        self.well_plate_grid = tk.Frame(self.well_plate, width=300, height=480, bg="lightgray")
        self.well_plate_grid.grid()
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
                self.well_buttons[index].grid(column=i, row=j)  # issue here when switching between well plates
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
            self.text_remaining_wells.set("You cannot select more wells") ### write in red pls
            self.remaining_wells.config(fg="red")
        else:
            self.text_remaining_wells.set("You can still select "+str(6-len(self.selected_wells))+" wells")
            self.remaining_wells.config(fg="black")
        
        
    def save_well_settings(self):
        self.settings["Well"]["Type"] = self.clicked.get()
        self.settings["Well"]["Number of well"] = len(self.selected_wells)
        for i in range(len(self.selected_wells)):
            self.settings["Well"][f"Culture {i+1}"] = self.selected_wells[i]    
        with open('TEST.json', 'w') as f:
            json.dump(self.settings, f, indent=4)
            
        # ici on garde les ancienne cultures en memoires, mais on a number of well qui est bien defini
        # pbm ou pas ?
      
    
    #### Functions related to the motion control tab ####   
    def set_tab_motion_control(self):
        tab_index = self.tabs_name.index("Motion Control")
        
        self.set_motor_control(tab_index)
        self.set_servo_control(tab_index)
        self.set_camera_for_control(tab_index)

                             
    def set_motor_control(self, tab_index):
        
        gui_x_pos = 0.15
        gui_y_pos = .5
        self.xyz_gui_position = ttk.Frame(self.tab[tab_index])
        self.xyz_gui_position.place(relx=gui_x_pos, rely=gui_y_pos, anchor=tk.CENTER)
        steps = [0.1, 1, 5, 10, 25, 50]
        coords_name = ["X", "Y", "Z"]
        
        self.pipette_selector_frame = ttk.Frame(self.tab[tab_index])
        self.pipette_selector_frame.place(relx=gui_x_pos+0.015, rely=0.15, anchor=tk.CENTER)
        pipette_name = list(self.settings.get("Offset").keys())[1:]
        
        self.pipette_selector_text = tk.Label(self.pipette_selector_frame, text="Select the toolhead's offset")
        self.pipette_selector_text.grid(column=0, row=0)
        
        self.clicked_pipette = tk.StringVar()
        self.pipette_offset_selector = tk.OptionMenu(self.pipette_selector_frame,
                                                     self.clicked_pipette,
                                                     *pipette_name,
                                                     command=self.select_offset)
        self.pipette_offset_selector.grid(column=0, row=1)
        
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
        
        
        self.z_label = tk.Label(self.xyz_gui_position, text=coords_name[2])
        self.z_label.grid(column=3, row=2, padx=10, pady=10)                      
        
        self.xyz_grid_steps = ttk.Frame(self.tab[tab_index])
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
        
        self.coord_value_grid = ttk.Frame(self.tab[tab_index])
        self.coord_value_grid.place(relx=gui_x_pos+0.015, rely= gui_y_pos+0.25, anchor=tk.CENTER)
        for i in range(len(coords_name)):
            self.coord_label.append(tk.Label(self.coord_value_grid, text=coords_name[i])) 
            self.coord_label[i].grid(column=i, row=5, padx=17, pady=10)
            
            self.coord_value_text.append(tk.StringVar())
            self.coord_value.append(tk.Entry(self.coord_value_grid, 
                                             width=7, 
                                             textvariable=self.coord_value_text[i],
                                             state='readonly'))  ### ajouter les vraies valeurs ici
            self.coord_value[i].grid(column=i, row=6, padx=17, pady=10)
        
        self.move_xyz_button = tk.Button(self.coord_value_grid, text="Move", command=lambda: self.move_xyz(move_button_cmd=True))
        self.move_xyz_button.grid(column=1, row=7, padx=17, pady=10)   
    
    
    def select_offset(self, value):
        self.offset = self.settings["Offset"][value]   
        ### TODO apply offset on position if homed   
        print(self.offset)        
     
    
    def move_xyz(self, x=0, y=0, z=0, move_button_cmd=False):
        ## maybe add a drop down menu with a list of every known position as to make everything faster
        ## maybe add a drop down menu setting the speeds !  
        if move_button_cmd:
            x = round(float(self.coord_value_text[0].get()),1)
            y = round(float(self.coord_value_text[1].get()),1)
            z = round(float(self.coord_value_text[2].get()),1)
        else:
            x = round(float(self.coord_value_text[0].get()) + x,1)
            y = round(float(self.coord_value_text[1].get()) + y,1)
            z = round(float(self.coord_value_text[2].get()) + z,1)
            
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
        self.anycubic.move_axis(x=x, y=y, z=z, offset=self.offset)
        self.coord_value_text[0].set(str(x))
        self.coord_value_text[1].set(str(y))
        self.coord_value_text[2].set(str(z))
        # Maybe find a way to read the coordinate instead of writing them manually into self.coord_value_text  
        
        
    def set_servo_control(self, tab_index):

        gui_x_pos = 0.85
        gui_y_pos = 0.5
        spacing = 20
        steps = [1, 5, 10, 25, 50, 100]
        
        button_height = 8
        self.servo_unit_text = tk.StringVar()
        self.servo_unit_text.set("Unit currently set to : steps")
        self.is_unit_percentage = False
        
        self.servo_gui_position = ttk.Frame(self.tab[tab_index])
        self.servo_gui_position.place(relx=gui_x_pos, rely=gui_y_pos, anchor=tk.CENTER)
        
        self.servo_unit_button = ttk.Button(self.tab[tab_index], 
                                            textvariable=self.servo_unit_text, 
                                            command=self.change_unit_servo)
        self.servo_unit_button.place(relx=gui_x_pos-0.033, rely=0.15, anchor=tk.CENTER)
        
        for i in range(len(self.servo_names)):
            self.servo_frame.append(ttk.Frame(self.servo_gui_position))
            self.servo_frame[i].grid(column=i, row=0, ipadx=spacing)
            
            self.servo_labels.append(tk.Label(self.servo_frame[i], text=self.servo_names[i]))
            self.servo_labels[i].grid(column=0, row=0, pady = 10)
            
            self.servo_buttons.append(ttk.Button(self.servo_frame[i], 
                                                 text="+", 
                                                 width=4,
                                                 command = lambda idx = i: self.move_servo('+', idx)))
            self.servo_buttons[2*i].grid(column=0, row=1, ipady=button_height)
            
            self.servo_buttons.append(ttk.Button(self.servo_frame[i], 
                                                 text="-", 
                                                 width=4,
                                                 command = lambda idx = i: self.move_servo('-', idx)))
            self.servo_buttons[2*i+1].grid(column=0, row=2, ipady=button_height)
            
            self.servo_values_text.append(tk.StringVar())
            self.servo_values_text[i].set(self.servo_pos[i])
            self.servo_values.append(tk.Label(self.servo_frame[i], textvariable=self.servo_values_text[i]))
            self.servo_values[i].grid(column=0, row=5, pady = 15)
            
        #### Buttons for deciding the values of the steps
        self.servo_grid_steps = ttk.Frame(self.tab[tab_index])
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
        self.save_position_gui = ttk.Frame(self.tab[tab_index])
        self.save_position_gui.place(relx=gui_x_pos-0.03, rely=gui_y_pos+0.3, anchor=tk.CENTER)   
        
        self.save_text = tk.Label(self.save_position_gui, text=f'''You can save the current positions of the motor and the servo.  \n They will be saved in the {SETTINGS} as : ''')
        self.save_text.grid(column=0, row=0)
        
        self.empty_label1 = tk.Label(self.save_position_gui, text=" ")
        self.empty_label1.grid(column=0, row=1)
        self.empty_label1.rowconfigure(1, minsize=2, weight=1)
        
        self.save_name_entry = tk.Entry(self.save_position_gui, width=15)
        self.save_name_entry.grid(column=0, row=2)
        self.empty_label2 = tk.Label(self.save_position_gui, text=" ")
        self.empty_label2.grid(column=0, row=3)
        self.empty_label2.rowconfigure(3, minsize=2, weight=1)
        self.save_pos_button = ttk.Button(self.save_position_gui, text="Save", command=self.save_pos)
        self.save_pos_button.grid(column=0, row=4)
     
     
    def move_servo(self, sign, idx):
        if not(self.is_unit_percentage) or idx == 2:
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
            # useless bug makes p2 go to 0, then its all fine
            if self.servo_pos[idx] > self.pipette_empty:
                self.servo_pos[idx] = self.pipette_empty
            elif self.servo_pos[idx] < 0:
                self.servo_pos[idx] = 0
            self.dynamixel.write_pipette_ul(volume_ul=self.servo_pos[idx], ID=idx+1)
            self.display_servo_pos()
        
        
    def set_camera_for_control(self, tab_index):
        self.camera_control_frame = tk.Frame(self.tab[tab_index])
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
    
        
    def change_unit_servo(self):
        if not(self.is_unit_percentage):
            self.servo_unit_text.set("Unit currently set to : percentage")
            self.is_unit_percentage = True
        else:
            self.servo_unit_text.set("Unit currently set to : steps")
            self.is_unit_percentage = False
        self.display_servo_pos()
            
    
    def display_servo_pos(self):
        
        if self.is_unit_percentage:
            self.servo_values_text[0].set(str(round(self.servo_pos[0]/self.pipette_empty*100,1))+"%")
            self.servo_values_text[1].set(str(round(self.servo_pos[1]/self.pipette_empty*100,1))+"%")   
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
        # ajouter un autre truc pour si on est avec les servos
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
        self.settings['Saved Positions'][var]["X"] = 'test'
        self.settings['Saved Positions'][var]["Y"] = 'test'
        self.settings['Saved Positions'][var]["Z"] = 'test'
        self.settings['Saved Positions'][var]["Servo 1"] = 'test'
        self.settings['Saved Positions'][var]["Servo 2"] = 'test'
        self.settings['Saved Positions'][var]["Servo Selector"] = 'test'        
        
            
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
        window.update()
        window.update_idletasks()

## peut etre un bouton pour reset les positions des servos
