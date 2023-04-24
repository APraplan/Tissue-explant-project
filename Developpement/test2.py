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
dyna.write_profile_velocity(100, ID="all")
dyna.set_position_gains(P_gain = 2500, I_gain = 60, D_gain = 5000, ID = 1)
# turn : 4096
    
PIPETTE_MIN = 280
PIPETTE_MAX = 2800

percentage = 0

while True:
    
    if keyboard.is_pressed('right'):
        print('Position ', percentage)
        # percentage = 0
        percentage = percentage + .2
        dir = 'Down'

    if keyboard.is_pressed('left'):
        print('Position ', percentage)
        # percentage = 100
        percentage = percentage - .2
        dir = 'Up'
        
    if keyboard.is_pressed('up'):
        print('Position ', percentage)
        percentage = 0
        dir = 'Up'

    if keyboard.is_pressed('down'):
        print('Position ', percentage)
        percentage = 100
        dir = 'Down'
                
    if keyboard.is_pressed('esc'):
        break
    
    dyna.write_pipette(percentage, ID=1)
    
    print('Position: ', dyna.read_position(ID=1), ' Desired position: ', PIPETTE_MIN + percentage/100.0*(PIPETTE_MAX-PIPETTE_MIN))
    
    sleep(0.02)
    
print('Goodby ;)')   
