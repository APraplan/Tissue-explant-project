import sys
import time
# sys.path.append("Platform")

sys.path.append(sys.path[0] + '\\..\\')
print("path is ", sys.path[-1])
from Platform.Communication.dynamixel_controller import Dynamixel
from Platform.Communication.ports_gestion import *


Dynamixel = Dynamixel(ID=[1,2,3], 
                            descriptive_device_name="XL430 test motor", 
                            series_name=["xl", "xl", "xl"], 
                            baudrate=57600,
                            pipette_max_ul = 680,
                            pipette_empty=670,    
                            port_name=get_com_port("0403", "6014"))
Dynamixel.begin_communication()
Dynamixel.set_operating_mode("position", ID="all")
Dynamixel.write_profile_velocity(100, ID="all")
Dynamixel.set_position_gains(P_gain = 2700, I_gain = 50, D_gain = 5000, ID=1)
Dynamixel.set_position_gains(P_gain = 2700, I_gain = 90, D_gain = 5000, ID=2)
Dynamixel.set_position_gains(P_gain = 2500, I_gain = 40, D_gain = 5000, ID=3)
        
# Dynamixel.select_tip(2,3)

# start = time.time()
# while time.time()-start <1:
#     pass
# print(Dynamixel.read_tip())

pos = [*Dynamixel.read_pos_in_ul(ID=[1,2]),30]
pos[0] = round(pos[0],0)
pos[1] = round(pos[1],0)
print(pos)