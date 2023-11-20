import tkinter as tk                     
from tkinter import ttk 
import json

import sys

sys.path.append('Platform')
sys.path.append('Pictures')
sys.path.append('Communication')
    
from Communication.ports_gestion import *

debug = True

if debug:
    from Communication.fake_communication import * 
else:
    from Communication.dynamixel_controller import *
    from Communication.printer_communications import * 

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
        # eventuellement ajouter des class pour les boutons, pour mieux gerer les scenarios, dui gnre les well plate button
        self.create_variables()
        self.window = tk.Tk()

        
        self.window.protocol("WM_DELETE_WINDOW", self.close_window)
        self.window.geometry("1200x700")
        self.window.title("X-Plant control panel")

        self.title = tk.Label(self.window, text="X-plant", font=("Arial Bold", 18))
        self.title.grid()

        # Create a style to configure the notebook
        self.style = ttk.Style()
        self.style.configure("TNotebook.Tab", padding=(15, 10))  # Adjust the padding values as needed
        
        self.style.configure('cameraStyle.TFrame', background="black")  

        self.tabControl = ttk.Notebook(self.window)

        for i in range(len(self.tabs_name)):
            self.tab.append(ttk.Frame(self.tabControl))
            self.tabControl.add(self.tab[i], text=self.tabs_name[i])
            self.set_tabs(i)
        self.tabControl.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")  # Adjust as needed
        self.window.columnconfigure(0, minsize=400, weight=1)
        self.window.rowconfigure(1, minsize=400,weight=1)

        self.window.mainloop()
        
        
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
        self.tab_orders = [0,1,2,3,4]  # each function will call this with self.tab_orders[i]. If you want to change
        # the orders of the tabs, for example for debugging, change the order here
        self.tab        = []
        self.title      = []
        self.style      = None
        self.tabControl = None
        
        self.tabs_name      = ["Mode", "Cameras", "Parameters", "Well plate", "XYZ Control"]
        
        self.options        = ["TPP6", "TPP12", "TPP24", "TPP48", "NUNC48", "FALCON48"]
        self.label_col      = ["A", "B", "C", "D", "E", "F"]
        self.label_row      = ["1", "2", "3", "4", "5", "6", "7", "8"]
        self.layout         = [[2,3], [3,4], [4,6], [6,8], [6,8], [6,8]]
        self.selected_wells = []
        self.well_dim_x     = 300
        self.well_dim_y     = 480
        self.drop           = None
        
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
        self.servo_unit_value   = 'steps'
        self.servo_step_buttons = []
        self.servo_grid_steps   = None
        self.servo_step         = 1
        self.servo_pos          = []
        
        self.servo_names    = ["Servo pipette 1", "Servo pipette 2", "Servo pipette selector"]
        
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
        self.tip_number = 0
        self.pipette_empty=525
        self.dynamixel.select_tip(tip_number=self.tip_number, ID=3)
        self.dynamixel.write_pipette_ul(self.pipette_empty, ID=[1,2])
        self.servo_pos = [self.pipette_empty, self.pipette_empty, 0]
        # self.dynamixel.select_tip(tip_number=1, ID=3)
             
        
    def load_parameters(self):
        with open(SETTINGS, 'r') as f:
            self.settings = json.load(f)
        
        
    def set_tabs(self, i):
        if i == 0:
            self.set_tab_mode()
        elif i == 1:
            self.set_tab_cameras()
        elif i == 2:
            self.set_tab_parameters()
        elif i == 3:
            self.set_tab_well_plate()
        elif i == 4:
            self.set_tab_xyz_control()
            
                  
    def debug(self, *args):
        
        print(args)
        
                 
    def set_tab_mode(self):
        None
        
        
    def set_tab_cameras(self):
        None
        
        
    def set_tab_parameters(self):
        # TODO
        tab_index = self.tab_orders[2]
        self.parameter_frame = tk.Frame(self.tab[tab_index])
        self.parameter_frame.pack()
        
        columns = ["Parameter", "Value"]
        self.parameter_threeview = ttk.Treeview(self.parameter_frame, columns=columns, show="headings")
        self.parameter_threeview.pack()
        
        
    def set_tab_well_plate(self):
        
        tab_index = self.tab_orders[3]
        
        self.clicked = tk.StringVar()
        self.clicked.set(" ")
        
        self.drop = ttk.OptionMenu(self.tab[tab_index], ## eventuellement changer pour un combobox.
                                  self.clicked,
                                  self.options[0],
                                  *self.options,
                                  command=self.show_wells)    
             
        # self.drop = ttk.Combobox(self.tab[tab_index], ## eventuellement changer pour un combobox.
        #                          state="readonly",
        #                          values=self.options,
        #                          command=self.show_wells) #look how to bind command to combobox
        self.drop.place(relx=0.3, rely=0.3, anchor=tk.CENTER)
        
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
        tab_index = self.tab_orders[3]
        self.selected_well_plate = click
        if self.well_plate_label is not None: # check if it exists
            self.well_plate_label.place_forget()
            self.selected_wells = []
            self.text_well_results.set("")
            self.text_remaining_wells.set("")
            for i in range(len(self.well_buttons)):
                self.well_buttons[i].grid_forget()
            self.well_buttons = []
            self.selected_wells = []
            
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
            
         
    def delete_well_plate(self):
        self.well_plate_label.place_forget()
        self.well_plate.place_forget() 
        
        
    def save_well_settings(self):
        self.settings["Well"]["Type"] = self.clicked.get()
        self.settings["Well"]["Number of well"] = len(self.selected_wells)
        for i in range(len(self.selected_wells)):
            self.settings["Well"][f"Culture {i+1}"] = self.selected_wells[i]    
        with open('TEST.json', 'w') as f:
            json.dump(self.settings, f, indent=4)
            
        # ici on garde les ancienne cultures en memoires, mais on a number of well qui est bien defini
        # pbm ou pas ?
      
        
    def set_tab_xyz_control(self):
        tab_index = self.tab_orders[4]
        
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
        self.servo_unit_value = 'steps'
        
        self.servo_gui_position = ttk.Frame(self.tab[tab_index])
        self.servo_gui_position.place(relx=gui_x_pos, rely=gui_y_pos, anchor=tk.CENTER)
        
        self.servo_temp_warning = ttk.Label(self.tab[tab_index], text="!! This button is currently useless, please ignore it !!")
        self.servo_temp_warning.place(relx=gui_x_pos-0.033, rely=0.1, anchor=tk.CENTER)
        self.servo_unit_button = ttk.Button(self.tab[tab_index], textvariable=self.servo_unit_text, command=self.change_unit_servo)
        self.servo_unit_button.place(relx=gui_x_pos-0.033, rely=0.15, anchor=tk.CENTER)
        
        for i in range(3):
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
        
        ## add buttons for the servo pipette selector
        
        ## add a button lock when at limit ?
        if idx == 2:
            ## TODO add maybe a way to still control this servo's position freely
            return
        
        # useless bug makes p2 go to 0, then its all fine
        delta = self.servo_step*(1 if sign == '+' else -1)
        
        self.servo_pos[idx] = self.servo_pos[idx] + delta
        if self.servo_pos[idx] > self.pipette_empty:
            self.servo_pos[idx] = self.pipette_empty
        elif self.servo_pos[idx] < 0:
            self.servo_pos[idx] = 0
        self.dynamixel.write_pipette_ul(volume_ul=self.servo_pos[idx], ID=idx+1)
        self.servo_values_text[idx].set(self.servo_pos[idx])
        
        
    def set_camera_for_control(self, tab_index):
        self.camera_control_frame = tk.Frame(self.tab[tab_index])
        self.camera_control_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  
        
        options = ["Camera 1", "Camera 2"]
        self.clicked_camera_control= tk.StringVar()
        self.camera_menu = tk.OptionMenu(self.camera_control_frame, 
                                          self.clicked_camera_control, 
                                          *options, 
                                          command=self.show_camera_control)
        
        self.camera_menu.pack()
            # self.camera_frame = tk.Canvas(self.camera_control_frame, width=300, height=300)
            # self.camera_frame.pack()
            # self.camera_frame.create_rectangle(0, 0, 300, 300, fill="lightgray")
    
    
    def show_camera_control(self, click):
        pass
    
        
    def change_unit_servo(self):
        if self.servo_unit_text.get() == "Unit currently set to : steps":
            self.servo_unit_text.set("Unit currently set to : percentage")
            self.servo_unit_value = 'percentage'
        else:
            self.servo_unit_text.set("Unit currently set to : steps")
            self.servo_unit_value = 'steps'
     
          
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
        self.window.destroy()
        
window = MyWindow()


## ajouter le fait que d'ecrire dans la box bouge limprimante
## tout pareil avec les servos
## peut etre un bouton pour reset les positions des servos
