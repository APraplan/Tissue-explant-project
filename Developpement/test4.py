import sys
sys.path.append('c:/Users/APrap/Documents/CREATE/Pick-and-Place')
from Platform.Communication.printer_communications import *

anycubic = Printer(descriptive_device_name="printer", port_name="COM10", baudrate=115200)


anycubic.connect()
anycubic.homing()