import sys
sys.path.append('Platform')
sys.path.append('Pictures')
sys.path.append('TEP_convNN_BW')
from Platform.platform_lib import platform_pick_and_place


platform = platform_pick_and_place()

platform.init()

platform.calibrate()

platform.run()

platform.disconnect()

