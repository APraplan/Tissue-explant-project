import sys
import platform
if platform.system() == 'Windows':
    sys.path.append('Platform')
    sys.path.append('Pictures')
    sys.path.append('TEP_convNN_96')
    sys.path.append('Developpement')
elif platform.system() == 'Linux':
    sys.path.append(sys.path[0]+'/Platform')
    # sys.path.append(sys.path[0]+'/Pictures/*')
    # sys.path.append(sys.path[0]+'/TEP_convNN_96')


    # sudo chmod a+rw /dev/ttyUSB0 if connection issues (Errno 13)
from Platform.platform_lib import platform_pick_and_place


platform = platform_pick_and_place()

platform.init()

platform.calibrate()

platform.run()

platform.disconnect()



