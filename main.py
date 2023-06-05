import sys
sys.path.append('Platform')
sys.path.append('Pictures')
sys.path.append('TEP_convNN_92')
from Platform.platform_lib import platform_pick_and_place


platform = platform_pick_and_place(com_printer='COM17', com_dynamixel='COM12', cam_head=0, cam_macro=1)

platform.init()

platform.calibrate()

platform.run()

platform.disconnect()

