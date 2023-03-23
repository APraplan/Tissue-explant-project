from dynamixel_controller import Dynamixel
from time import sleep
import keyboard
import math

dyna = Dynamixel(ID=[1], descriptive_device_name="XL430 test motor", series_name=["xl"], baudrate=57600,
                 port_name="COM12")

dyna.begin_communication()
# dyna.set_operating_mode("position", ID=1)
dyna.set_operating_mode("position", ID=1)
# dyna.write_profile_acceleration(5, ID="all")
dyna.write_profile_velocity(10, ID="all")
# turn : 4096

# 0 = 2158
# 100 = 2638

position = 2158

def linearisation(percentage):
    
    if percentage < 0:
        percentage = 0
    if percentage > 100:
        percentage = 100
    
    max = math.cos(2648*math.pi/4096)
    min = math.cos(2158*math.pi/4096)
    
    return math.acos(min + percentage/100.0*(max-min))/math.pi*4096
    
    

while True:
    
    if keyboard.is_pressed('right'):
        print('Position ', position)
        position = 0
        # position = position + 10

    if keyboard.is_pressed('left'):
        print('Position ', position)
        position = 100
        # position = position -10
        
    if keyboard.is_pressed('esc'):
        break
    
    dyna.write_position(linearisation(position), ID=1)   
    
    sleep(0.02)
    
print('Goodby ;)')   
    
dyna.end_communication()