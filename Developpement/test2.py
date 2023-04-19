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
dyna.write_profile_velocity(20, ID="all")
# turn : 4096

# 0 = 2158
# 100 = 2638

position = 2158
percentage = 0
error = 0
correction = 0
sum_error = 0
past_error = 0

def linearisation(percentage, dir):
    
    if percentage < 0:
        percentage = 0
    if percentage > 100:
        percentage = 100
    
    max = math.cos(2648*math.pi/4096)
    min = math.cos(2158*math.pi/4096)
    
    if dir == 'Down':
        return 1.015*math.acos(min + percentage/100.0*(max-min))/math.pi*4096
    else:
        return 1.005*math.acos(min + percentage/100.0*(max-min))/math.pi*4096
    
   
dir = 'Up' 

while True:
    
    if keyboard.is_pressed('right'):
        print('Position ', percentage)
        # percentage = 0
        percentage = percentage + 10
        dir = 'Down'

    if keyboard.is_pressed('left'):
        print('Position ', percentage)
        # percentage = 100
        percentage = percentage - 10
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
    
    pos = linearisation(percentage, dir)
    dyna.write_position(pos, ID=1)
    # dyna.write_position(linearisation(percentage)+error, ID=1)   
    
    # print('Pos ', dyna.read_pipette_pos(ID=1))
    
    # Ki = 0.2
    # Kd = 0.5
    
    # error = linearisation(percentage) - dyna.read_position(ID=1)
    
    # sum_error = sum_error + error
    # if sum_error <= -60/Ki:
    #     sum_error = -60/Ki
    # if sum_error >= 60/Ki:
    #     sum_error = 60/Ki
        
    # correction = Ki * sum_error + Kd*(error - past_error)
    # past_error = error 
    
    # dyna.write_position(linearisation(percentage)+correction, ID=1)  
    
    print('Position: ', dyna.read_position(ID=1), ' Desired position: ', linearisation(percentage, 'Up'), ' Send ', pos)
    
    sleep(0.02)
    
print('Goodby ;)')   

# dyna.set_operating_mode("velocity", ID=1)

# P = 0
# I = 0
# D = 0

# error = 0
# sum_error = 0
# past_error = 0
# position = linearisation(0)
# speed = 0
# antiwindup = 20

# while True:
   
#     if keyboard.is_pressed('right'):
#         print('Position ', percentage)
#         # percentage = 0
#         percentage = percentage + 1

#     if keyboard.is_pressed('left'):
#         print('Position ', percentage)
#         # percentage = 100
#         percentage = percentage - 1

#     if keyboard.is_pressed('u'):
#         print('P ', P)
#         # percentage = 100
#         P = P + 0.01
        
#     if keyboard.is_pressed('j'):
#         print('P ', P)
#         # percentage = 0
#         P = P - 0.01

#     if keyboard.is_pressed('i'):
#         print('I ', I)
#         # percentage = 100
#         I = I + 0.01
        
#     if keyboard.is_pressed('k'):
#         print('I ', I)
#         # percentage = 0
#         I = I - 0.01

#     if keyboard.is_pressed('o'):
#         print('D ', D)
#         # percentage = 100
#         D = D + 0.01
        
#     if keyboard.is_pressed('l'):
#         print('D ', D)
#         # percentage = 0
#         D = D - 0.01
                
#     if keyboard.is_pressed('esc'):
#         break
    
#     position = linearisation(percentage)
    
#     try:
#         error = position - dyna.read_position(ID=1)
        
#         sum_error = sum_error + error
#         if sum_error < -antiwindup:
#             sum_error = -antiwindup
#         elif sum_error > antiwindup:
#             sum_error = antiwindup
        
#         diff_error = error - past_error
#         past_error = error
        
#         speed = int(P*error+I*sum_error+D*diff_error)
        
#         dyna.write_velocity(speed, ID=1)
#     except:
#         print('error')
    
# dyna.end_communication()