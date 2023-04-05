import sys
sys.path.append('c:/Users/APrap/Documents/CREATE/Pick-and-Place/Platform')
from Platform.interface_functions import *


platform = platform_pick_and_place()

platform.init()

platform.run()

platform.disconnect()