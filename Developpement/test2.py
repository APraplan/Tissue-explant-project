import sys
sys.path.append('c:/Users/APrap/Documents/CREATE/Pick-and-Place')

from Platform.Communication.dynamixel_controller import Dynamixel
from time import sleep
import keyboard
import math

dyna = Dynamixel(ID=[1,2,3], descriptive_device_name="XL430 test motor", series_name=["xl", "xl", "xl"], baudrate=57600,
                 port_name="COM12")

dyna.begin_communication()
# dyna.set_operating_mode("position", ID=1)
dyna.set_operating_mode("position", ID="all")
# dyna.write_profile_acceleration(5, ID="all")
dyna.write_profile_velocity(100, ID="all")
dyna.set_position_gains(P_gain = 2500, I_gain = 60, D_gain = 5000, ID = [1, 2])
# turn : 4096
    
PIPETTE_MIN = 280
PIPETTE_MAX = 2800

tip_num = 0
percentage_1 = 0
percentage_2 = 0
# pos = 0121221212

while True:
    
    if keyboard.is_pressed('right'):
        print('Position ', percentage_2)
        # position += 10
        percentage_2 = 0

    if keyboard.is_pressed('left'):
        print('Position ', percentage_2)
        # position -= 10
        percentage_2 = 100
        
    if keyboard.is_pressed('up'):
        print('Position ', percentage_1)
        percentage_1 = 0

    if keyboard.is_pressed('down'):
        print('Position ', percentage_1)
        percentage_1 = 100
        
    if keyboard.is_pressed("z"):
        print('Tip ', tip_num)
        tip_num = 0
        
    if keyboard.is_pressed("o"):
        tip_num = 1
        print('Tip ', tip_num)
        # pos += 10

    if keyboard.is_pressed("t"):
        tip_num = 2
        print('Tip ', tip_num)
        # pos -= 10
                
    if keyboard.is_pressed('esc'):
        break
    
    # dyna.write_position(pos, ID=3)
    dyna.write_pipette(percentage_1, ID=1)
    dyna.write_pipette(percentage_2, ID=2)
    dyna.select_tip(tip_num, ID=3)
    
    # print('Position: ', dyna.read_position(ID=3)01201201,11 ' Desired position: ', PIPETTE_MIN + percentage/100.0*(PIPETTE_MAX-PIPETTE_MIN))
    
    sleep(0.02)
    
print('Goodby ;)')   
