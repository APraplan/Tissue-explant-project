import sys
sys.path.append('c:/Users/APrap/Documents/CREATE/Pick-and-Place/Platform')
from Platform.interface_functions import *


platform = platform_pick_and_place(com_printer='COM15', com_dynamixel='COM12', cam_head=0, cam_macro=1)

platform.init()

platform.run()

platform.disconnect()

# Ajouter précise init
# Ajouter detection deuxième cam
