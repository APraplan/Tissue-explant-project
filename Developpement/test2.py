import sys
sys.path.append(r"C:\Users\APrap\Documents\CREATE\Tissue-explant-project")

from Platform.Communication.dynamixel_controller import Dynamixel
from time import sleep
import keyboard

dyna = Dynamixel(ID=[1,2,3], descriptive_device_name="XL430 test motor", series_name=["xl", "xl", "xl"], baudrate=57600,
                 port_name="COM5")

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
volume = 0

while True:
    
    if keyboard.is_pressed('0'):
        print('Position ', volume)
        volume = 0
    
    if keyboard.is_pressed('1'):
        print('Position ', volume)
        volume = 100

    if keyboard.is_pressed('2'):
        print('Position ', volume)
        volume = 200
        
    if keyboard.is_pressed('3'):
        print('Position ', volume)
        volume = 300

    if keyboard.is_pressed('4'):
        print('Position ', volume)
        volume = 400
        
    if keyboard.is_pressed('5'):
        print('Position ', volume)
        volume = 600
        
    if keyboard.is_pressed("z"):
        print('Tip ', tip_num)
        tip_num = 0
        
    if keyboard.is_pressed("o"):
        tip_num = 1
        print('Tip ', tip_num)

    if keyboard.is_pressed("t"):
        tip_num = 2
        print('Tip ', tip_num)
                
    if keyboard.is_pressed('esc'):
        break
    
    # dyna.write_position(pos, ID=3)
    if tip_num == 1:
        dyna.write_pipette_ul(volume, ID=1)
    if tip_num == 2:
        dyna.write_pipette_ul(volume, ID=2)
        
    dyna.select_tip(tip_num, ID=3)
    
    # print('Position: ', dyna.read_position(ID=3)01201201,11 ' Desired position: ', PIPETTE_MIN + percentage/100.0*(PIPETTE_MAX-PIPETototzotoztttttTE_MIN))
    
    sleep(0.02)
    
print('Goodby ;)')   