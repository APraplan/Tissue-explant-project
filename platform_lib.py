import numpy as np

PETRI_DISH_HEIGHT = 20
PETRI_DISH_PICK_HEIGHT = 0
PETRI_DISH_X_POSITION = 50
PETRI_DISH_Y_POSITION = 100
PETRI_DISH_RADIUS = 30

TEST_TUBE_HEIGHT = 50
TEST_TUBE_PLACE_HEIGHT = 30
TEST_TUBE_X_POSITION = 150
TEST_TUBE_Y_POSITION = 100
TEST_TUBE_X_MIN = 120
TEST_TUBE_X_MAX = 180
TEST_TUBE_Y_MIN = 60
TEST_TUBE_Y_MAX = 140
NUMBER_TUBE_X = 5
NUMBER_TUBE_Y = 10
OFFSET_TUBE = 5


TEST_TUBE_N = np.array([1, 0, 0])
TEST_TUBE_P0 = np.array([TEST_TUBE_X_MIN, 0, 0])

class tissue:
    
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        
class petri_dish:
    def __init__(self, x, y, z, pick_z, r):
        self.x = x
        self.y = y
        self.z = z 
        self.pick_z = pick_z
        self.r = r 
        
class test_tube:
    def __init__(self, x1, y1, z, place_z, min_x, max_x, min_y, max_y, num_x, num_y, offset_tube):
        self.x1 = x1
        self.y1 = y1
        self.z = z
        self.place_z = place_z
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y 
        self.max_y = max_y
        self.num_x = num_x
        self.num_y = num_y 
        self.offset_tube = offset_tube
        self.number_sample = 0
    
    def destination(self):
        mod = int(self.number_sample/self.num_y)
        
        if mod == self.num_x -1:
            print('Test tube full !')
            return 
        else:
            return self.x1-self.offset_tube*mod, self.y1+self.offset_tube*(self.number_sample - mod*self.num_y)
        
    def add_one_sample(self):
        self.number_sample += 1
        

petri = petri_dish(PETRI_DISH_X_POSITION, PETRI_DISH_Y_POSITION, PETRI_DISH_HEIGHT, PETRI_DISH_PICK_HEIGHT, PETRI_DISH_RADIUS) 

tube = test_tube(TEST_TUBE_X_POSITION, TEST_TUBE_Y_POSITION, TEST_TUBE_HEIGHT, TEST_TUBE_PLACE_HEIGHT, TEST_TUBE_X_MIN, TEST_TUBE_X_MAX, TEST_TUBE_Y_MIN, TEST_TUBE_Y_MAX, NUMBER_TUBE_X, NUMBER_TUBE_Y, OFFSET_TUBE)   
        