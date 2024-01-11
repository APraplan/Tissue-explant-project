
import sys
import platform

if platform.system() == 'Windows':
    sys.path.append('Platform')
    sys.path.append('Pictures')
    sys.path.append('TEP_convNN_96')
    sys.path.append('Developpement')
elif platform.system() == 'Linux':
    sys.path.append(sys.path[0]+'/Platform')
    
from Platform.platform_lib import platform_pick_and_place
from Platform.test_new_gui import MyWindow
import Developpement.Cam_gear as cam_gear
    
window = MyWindow()


# while window.isOpen:
#     window.update_cameras()
#     window.update()
#     window.update_idletasks()

window.debug()
window.mainloop()