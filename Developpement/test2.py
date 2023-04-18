import sys
sys.path.append('c:/Users/APrap/Documents/CREATE/Pick-and-Place')

from Platform.Communication.dynamixel_controller import Dynamixel
from time import sleep
import keyboard
import math

dyna = Dynamixel(ID=[1], descriptive_device_name="XL430 test motor", series_name=["xl"], baudrate=57600,
                 port_name="COM12")

dyna.begin_communication()
# dyna.set_operating_mode("position", ID=1)
dyna.set_operating_mode("position", ID=1)
# dyna.write_profile_acceleration(5, ID="all")
dyna.write_profile_velocity(60, ID="all")
# turn : 4096

# 0 = 2158
# 100 = 2638

position = 2158
percentage = 0
error = 0

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
        print('Position ', percentage)
        # percentage = 0
        percentage = percentage + 1

    if keyboard.is_pressed('left'):
        print('Position ', percentage)
        # percentage = 100
        percentage = percentage - 1
                
    if keyboard.is_pressed('esc'):
        break
    
    dyna.write_position(linearisation(percentage)+error//2, ID=1)   
    
    error = error + linearisation(percentage) - dyna.read_position(ID=1)
    if error <= -80:
        error = -80
    if error >= 80:
        error = 80
    
    print('Position: ', dyna.read_position(ID=1), ' Desired position: ', linearisation(percentage), ' Send: ', linearisation(percentage)+error//2)
    
    sleep(0.02)
    
print('Goodby ;)')   
    
dyna.end_communication()