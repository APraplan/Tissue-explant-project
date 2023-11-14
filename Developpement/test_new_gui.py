import tkinter as tk                     
from tkinter import ttk 


class ArrowButtonRight(tk.Frame):  ## replace these with pictures
    def __init__(self, master=None, size=40, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        self.canvas = tk.Canvas(self, width=size, height=size)
        self.canvas.create_polygon(7, 7, 35, 20, 7, 33, fill="black", outline="black")
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.grid()

    def on_click(self, event):
        print("Right Arrow Button clicked!")

class ArrowButtonTop(tk.Frame):
    def __init__(self, master=None, size=40, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        self.canvas = tk.Canvas(self, width=size, height=size)
        self.canvas.create_polygon(7, 33, 20, 7, 33, 33, fill="black", outline="black")
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.pack()

    def on_click(self, event):
        print("Top Arrow Button clicked!")

class ArrowButtonLeft(tk.Frame):
    def __init__(self, master=None, size=40, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        self.canvas = tk.Canvas(self, width=size, height=size)
        self.canvas.create_polygon(7, 20, 35, 7, 35, 33, fill="black", outline="black")
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.pack()

    def on_click(self, event):
        print("Left Arrow Button clicked!")

class ArrowButtonBottom(tk.Frame):
    def __init__(self, master=None, size=40, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        self.canvas = tk.Canvas(self, width=size, height=size)
        self.canvas.create_polygon(7, 7, 20, 33, 33, 7, fill="black", outline="black")
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.pack()

    def on_click(self, event):
        print("Bottom Arrow Button clicked!")

class RoundButton(tk.Canvas):
    def __init__(self, master=None, diameter=50, bg_color="lightgray", **kwargs):
        tk.Canvas.__init__(self, master, width=diameter, height=diameter, bg=bg_color, highlightthickness=0, **kwargs)
        self.diameter = diameter

        # Draw a circle on the canvas
        radius = diameter // 2
        self.create_oval(0, 0, diameter, diameter, outline="black", fill=bg_color)

        self.bind("<Button-1>", self.on_click)

    def on_click(self, event):
        print("Round Button Clicked!")
        
        

class MyWindow:
    def __init__(self):
        
        self.window = tk.Tk()

        self.window.geometry("1200x700")
        self.window.title("X-Plant control panel")

        self.tabs_name = ["Mode", "Cameras", "Parameters", "Well plate", "XYZ Control"]

        self.label = tk.Label(self.window, text="X-plant", font=("Arial Bold", 18))
        self.label.grid()

        # Create a style to configure the notebook
        self.style = ttk.Style()
        self.style.configure("TNotebook.Tab", padding=(15, 10))  # Adjust the padding values as needed


        self.tabControl = ttk.Notebook(self.window)

        self.tab = []
        for i in range(len(self.tabs_name)):
            self.tab.append(ttk.Frame(self.tabControl))
            self.tabControl.add(self.tab[i], text=self.tabs_name[i])
            self.set_tabs(i)
        self.tabControl.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")  # Adjust as needed
        self.window.columnconfigure(0, minsize=400, weight=1)
        self.window.rowconfigure(1, minsize=400,weight=1)

        
        self.window.mainloop()

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
            
    def set_tab_mode(self):
        None
        
    def set_tab_cameras(self):
        None
        
    def set_tab_parameters(self):
        None
        
    def set_tab_well_plate(self):
        
        tab_index = 0
        options = ["TPP6", "TPP12", "TPP24", "TPP48", "NUNC48", "FALCON48"]
        
        self.clicked = tk.StringVar()
        self.clicked.set(options[0])
        
        self.drop = tk.OptionMenu(self.tab[tab_index] , self.clicked , *options ) 
        self.drop.place(relx=0.3, rely=0.3, anchor=tk.CENTER)
        
        self.well_plate_label = tk.Label(self.tab[tab_index], text=self.clicked.get())  ## trouver une maniere de update ce label
        self.well_plate_label.place(relx=0.7, rely=0.05, anchor=tk.CENTER)
        self.well_plate = tk.Frame(self.tab[tab_index], width=300, height=500, bg="lightgray")
        self.well_plate.place(relx=0.7, rely=0.5, anchor=tk.CENTER)
        
        self.set_well_plate()
        
    def set_well_plate(self):
        None
        
    def set_tab_xyz_control(self):
        tab_index = 4
        
        self.set_motor_control(tab_index)
        self.set_servo_control(tab_index)
            
        
        col_count, row_count = self.tab[tab_index].grid_size()
        
        for col in range(col_count):
            self.tab[tab_index].grid_columnconfigure(col, minsize=20)
        for row in range(row_count):
            self.tab[tab_index].grid_rowconfigure(row, minsize=20)
                
                
    def set_motor_control(self, tab_index):
        
        row_offset = 8
        col_offset = 5
        steps = [0.1, 1, 5, 10, 25, 50]
        coords_name = ["X", "Y", "Z"]
        
        # self.button = tk.Button(self.tab[i], text="Quit", command=self.window.quit).grid(column=0, row=1, padx=10, pady=10)
        self.button_right = ArrowButtonRight(self.tab[tab_index])
        self.button_right.grid(column=2+col_offset, row=1+row_offset, padx=10, pady=10)
        
        self.button_left = ArrowButtonLeft(self.tab[tab_index])
        self.button_left.grid(column=0+col_offset, row=1+row_offset, padx=10, pady=10)
        
        self.button_top = ArrowButtonTop(self.tab[tab_index])
        self.button_top.grid(column=1+col_offset, row=0+row_offset, padx=10, pady=10)
        
        self.button_bottom = ArrowButtonBottom(self.tab[tab_index])
        self.button_bottom.grid(column=1+col_offset, row=2+row_offset, padx=10, pady=10)
        
        self.center_button = RoundButton(self.tab[tab_index], diameter=50, bg_color="black")
        self.center_button.grid(column=1+col_offset, row=1+row_offset, padx=10, pady=10)
        
        self.small_grid_steps = []
        self.step_buttons = []
        for i in range(3):
            self.small_grid_steps.append(ttk.Frame(self.tab[tab_index]))
            self.small_grid_steps[i].grid(column=col_offset+i+1, row=row_offset-1, columnspan=1)
            self.step_buttons.append(ttk.Button(self.small_grid_steps[i], text=str(steps[2*i]), width=5).grid(column=0, row=0))  ### set command here and show which step is selected
            self.step_buttons.append(ttk.Button(self.small_grid_steps[i], text=str(steps[2*i+1]), width=5).grid(column=1, row=0)) ### set command here
            
        
        self.z_button_up = ArrowButtonTop(self.tab[tab_index])
        self.z_button_up.grid(column=4+col_offset, row=0+row_offset, padx=10, pady=10)
        
        self.z_button_down = ArrowButtonBottom(self.tab[tab_index])
        self.z_button_down.grid(column=4+col_offset, row=2+row_offset, padx=10, pady=10)
        
        self.z_label = tk.Label(self.tab[tab_index], text=coords_name[2])
        self.z_label.grid(column=4+col_offset, row=1+row_offset, padx=10, pady=10)                      
        
        self.coord_label = []
        self.coord_value = []
        for i in range(len(coords_name)):
            self.coord_label.append(tk.Label(self.tab[tab_index], text=coords_name[i])) 
            self.coord_label[i].grid(column=i+col_offset+1, row=3+row_offset+2, padx=10, pady=10)
            
            self.coord_value.append(tk.Entry(self.tab[tab_index], width=7))  ### ajouter les vraies valeurs ici
            self.coord_value[i].grid(column=i+col_offset+1, row=3+row_offset+3, padx=10, pady=10)
        
            
    def set_servo_control(self, tab_index):

        row_offset = 8
        col_offset = 18
        spacing = 5
        
        button_height = 6
        
        servo_names = ["Servo pipette 1", "Servo pipette 2", "Servo pipette selector"]
        
        self.servo_buttons = []
        self.servo_frame = []
        self.servo_labels = []
        self.servo_values = []
        for i in range(3):
            self.servo_frame.append(ttk.Frame(self.tab[tab_index]))
            self.servo_frame[i].grid(column=i*spacing + col_offset, row=row_offset-1, columnspan=1, rowspan=6)
            
            self.servo_labels.append(tk.Label(self.servo_frame[i], text=servo_names[i]))
            self.servo_labels[i].grid(column=0, row=0, pady = 10)
            
            self.servo_buttons.append(ttk.Button(self.servo_frame[i], text="+", width=4).grid(column=0, row=1, ipady=button_height))
            self.servo_buttons.append(ttk.Button(self.servo_frame[i], text="-", width=4).grid(column=0, row=2, ipady=button_height))
            
            self.servo_values.append(tk.Label(self.servo_frame[i], text="0"))  ## to change for actual value, and hopes it get updated
            self.servo_values[i].grid(column=0, row=5, pady = 15)
        
            
window = MyWindow()