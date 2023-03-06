from movement_functions import *
from computer_vision import *

def pick_and_place():
    
    while True:
        take_picture()
    
        cell = get_cell_position()
        
        pick(cell)
    
        place(tube.destination()[0], tube.destination()[1])
        tube.add_one_sample()
    