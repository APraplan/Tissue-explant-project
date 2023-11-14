import tkinter as tk                     
from tkinter import ttk 


class ArrowButtonRight(tk.Frame):
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
        self.window.title("Test GUI")

        self.tabs_name = ["Mode", "cameras", "Parameters", "well plate", "XYZ Control"]

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
                # Change from pack to grid for self.tabControl
        self.tabControl.grid(row=1, column=0,columnspan=100,rowspan=100, padx=10, pady=10, sticky="nsew")  # Adjust as needed
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(1, weight=1)

        
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
        None
        
    def set_tab_xyz_control(self):
        tab_index = 0
        row_offset = 5
        col_offset = 10
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
        
        
window = MyWindow()