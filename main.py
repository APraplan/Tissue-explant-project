# from movement_functions import *
# from interface_functions import *

# test_multi()

# select_mode()

# disconnect_all()

from Platform.platform_lib import *


from Platform.Communication.printer_communications import *
from Platform.platform_lib import *
from Platform.Communication.dynamixel_controller import *
import Platform.computer_vision as cv

sys.path.append('../')

anycubic = printer(descriptive_device_name="printer", port_name="COM10", baudrate=115200)
dyna = Dynamixel(ID=[1], descriptive_device_name="XL430 test motor", series_name=["xl"], baudrate=57600,
                 port_name="COM12")
detector = cv.create_detector()
platform = platform_pick_and_place(anycubic=anycubic, dynamixel=dyna, detector=detector)

platform.start()