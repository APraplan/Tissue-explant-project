from loguru import logger

PIPETTE_MIN = [360, 3770]
PIPETTE_MAX = [2880, 1250]
TIP_POSITION = [3072, 2560, 3584]

class Dynamixel:
    def __init__(self, ID, descriptive_device_name, port_name, baudrate, series_name = "xm"):
        logger.debug(f"Initializing Dynamixel {ID} on port {port_name} with baudrate {baudrate}")
        self.ID = ID
        self.positions = {}
        
        if type(ID) == list:
            for id in ID:
                self.positions[id] = 0 
        else:
            self.positions[ID] = 0
                
    def begin_communication(self, enable_torque = True):
        logger.debug(f"Beginning communication with Dynamixel {self.ID}")

    def end_communication(self, disable_torque = True):
        logger.debug(f"Ending communication with Dynamixel {self.ID}")

    def enable_torque(self, print_only_if_error=False, ID = None):
        logger.debug(f"Enabling torque on Dynamixel {self.ID}")
        
    def disable_torque(self, print_only_if_error=False, ID = None):
        logger.debug(f"Disabling torque on Dynamixel {self.ID}")
        
    def set_operating_mode(self, mode, ID = None, print_only_if_error = False):
        logger.debug(f"Setting operating mode of Dynamixel {self.ID} to {mode}")
        
    def set_velocity_gains(self,  P_gain = None, I_gain = None, ID = None):
        logger.debug(f"Setting velocity gains of Dynamixel {self.ID} to P_gain = {P_gain}, I_gain = {I_gain}")
        
    def set_position_gains(self, P_gain = None, I_gain = None, D_gain = None, ID = None):
        logger.debug(f"Setting position gains of Dynamixel {self.ID} to P_gain = {P_gain}, I_gain = {I_gain}, D_gain = {D_gain}")
        
    def read_position(self, ID = None):
        return self.positions[ID]
            
    def read_velocity(self, ID = None):
        return 0

    def read_current(self, ID = None):
        return 0

    def read_pwm(self, ID = None):
        return 0

    def read_from_address(self, number_of_bytes, ADDR, ID = None):
        return

    def write_position(self, pos, ID = None):
        if type(ID) == list:
            for id in ID:
                self.positions[id] = pos
        else:
            self.positions[ID] = pos
            
    def write_velocity(self, vel, ID = None):
        pass
        
    def write_current(self, current, ID = None):
        pass
    
    def write_pwm(self, pwm, ID = None):
        pass
    
    def write_profile_velocity(self, profile_vel, ID = None):
        pass
    
    def write_profile_acceleration(self, profile_acc, ID = None):
        pass
    
    def write_to_address(self, value, number_of_bytes, ADDR, ID = None):
        pass
    
    def write_pipette(self, percentage, ID = None):
            
        if percentage > 100:
            percentage = 100
        elif percentage < 0:
            percentage = 0
            
        if type(ID) == list:
            for id in ID:
                pos = int(PIPETTE_MIN[id-1] + percentage/100.0*(PIPETTE_MAX[id-1]-PIPETTE_MIN[id-1]))
                self.write_position(pos=pos, ID = id)
        else:
            pos = int(PIPETTE_MIN[ID-1] + percentage/100.0*(PIPETTE_MAX[ID-1]-PIPETTE_MIN[ID-1]))
            self.write_position(pos=pos, ID = ID)
                  
    def pipette_is_in_position(self, percentage, ID = None):
        
        d_pos = int(PIPETTE_MIN[ID-1] + percentage/100.0*(PIPETTE_MAX[ID-1]-PIPETTE_MIN[ID-1]))
        
        a_pos = self.read_position(ID = ID)
        
        if abs(d_pos-a_pos) <= 4:
            return True
        else:
            return False
          
    def select_tip(self, tip_number, ID = None):
            self.write_position(pos=TIP_POSITION[tip_number], ID = id)       
        
    def write_pipette_ul(self, volume_ul, ID = None):
            
        if volume_ul > 625:
            volume_ul = 625
        elif volume_ul < 0:
            volume_ul = 0
            
        if type(ID) == list:
            for id in ID:
                pos = int(PIPETTE_MIN[id-1] + volume_ul/620.0*(PIPETTE_MAX[id-1]-PIPETTE_MIN[id-1]))
                self.write_position(pos=pos, ID = id) 
        else:
            pos = int(PIPETTE_MIN[ID-1] + volume_ul/620.0*(PIPETTE_MAX[ID-1]-PIPETTE_MIN[ID-1]))
            self.write_position(pos=pos, ID = ID)
            
    def pipette_is_in_position_ul(self, volume_ul, ID = None):
        
        d_pos = int(PIPETTE_MIN[ID-1] + volume_ul/620.0*(PIPETTE_MAX[ID-1]-PIPETTE_MIN[ID-1]))
        
        a_pos = self.read_position(ID = ID)
        
        if abs(d_pos-a_pos) <= 4:
            return True
        else:
            return False
        
    
import serial
from threading import Thread
from time import time, sleep
import sys

class Printer:
    def __init__(self, descriptive_device_name, port_name, baudrate):
        logger.debug("Initializing printer " + descriptive_device_name + " on port " + port_name + " with baudrate " + str(baudrate))
        self.descriptive_device_name = descriptive_device_name
        self.position = position(0,0,0)
        
        self.home_pos = position(0,0,0)
        self._finish = False

    def _serial_readline(self):
        while True:
            if not self._finish:
                logger.debug("Finished")
                self._finish = True

            sleep(0.1)

    def _start_Reading_Thread(self):
        self.__thread = Thread(target=self._serial_readline)
        self.__thread.daemon = True
        self.__thread.start()

    def connect(self, timeout = 20):
        self._start_Reading_Thread()
        logger.debug("Connecting to " + self.descriptive_device_name)

    def disconnect(self):
        logger.debug("Disconnecting from " + self.descriptive_device_name)

    def send_gcode(self, gcode, wait_until_completion = True, printMsg = True):
        logger.debug("Sending gcode: " + gcode)

    def max_x_feedrate(self, speed):
        self.send_gcode("M203 X" + str(float(speed)), printMsg=False)

    def max_y_feedrate(self, speed):
        self.send_gcode("M203 Y" + str(float(speed)), printMsg=False)
        
    def max_z_feedrate(self, speed):
        self.send_gcode("M203 Z" + str(float(speed)), printMsg=False)

    def stop_motion(self):
        self.send_gcode("M410", printMsg=False)

    def set_home_pos(self, x = 0, y = 0, z = 0):
        self.home_pos = position(x,y,z)

    def homing(self, printMsg=False):
        self.send_gcode("G28 R25", printMsg=printMsg)

    def move_home(self, f = 1000, printMsg=False):
        self.move_axis(x = self.home_pos[0], y = self.home_pos[1], z = self.home_pos[2], f = f, printMsg=printMsg)

    def move_axis_relative(self, x = None, y = None, z = None, e = None, f = None, printMsg = False):
        self._finish = False
        command = "G0"
        
        if x is not None:
            command = command + " X" + str(x + self.home_pos.x)
            self.position.x = self.home_pos.x + x
        if y is not None:
            command = command + " Y" + str(y + self.home_pos.y)
            self.position.y = self.home_pos.y + y  
        if z is not None:
            command = command + " Z" + str(z + self.home_pos.z)
            self.position.z = self.home_pos.z + z   
        if e is not None:
            command = command + " E" + str(e)
        if f is not None:
            command = command + " F" + str(float(f))

        self.send_gcode(command, wait_until_completion=False, printMsg=printMsg) 

    def move_axis(self, x = None, y = None, z = None, e = None, f = None, printMsg = False):
        self._finish = False
        command = "G0"
        
        if x is not None:
            command = command + " X" + str(x)
            self.position.x = x
        if y is not None:
            command = command + " Y" + str(y)
            self.position.y = y
        if z is not None:
            command = command + " Z" + str(z)
            self.position.z = z
        if e is not None:
            command = command + " E" + str(e)
        if f is not None:
            command = command + " F" + str(float(f))

        self.send_gcode(command, wait_until_completion=False, printMsg=printMsg)

    def move_axis_incremental(self, x = None, y = None, z = None, e = None, f = None, printMsg = False):
        self._finish = False
        command = "G0"
        position = self.read_position(printMsg=False)
        
        if x is not None:
            command = command + " X" + str(x + position[0])
            self.position.x = position.x + x
        if y is not None:
            command = command + " Y" + str(y + position[1])
            self.position.y = position.y + y
        if z is not None:
            command = command + " Z" + str(z + position[2])
            self.position.z = position.z + z
        if e is not None:
            command = command + " E" + str(e)
        if f is not None:
            command = command + " F" + str(float(f))

        self.send_gcode(command, wait_until_completion=True, printMsg=printMsg)

    def read_position(self, printMsg=False):
        return self.position                
                
    def read_position_relative(self, printMsg=False):
        pos = self.read_position()
        pos.x += self.home_pos.x
        pos.y += self.home_pos.y
        pos.z += self.home_pos.z    
        
        if printMsg:
            print("position:", pos.x, pos.y, pos.z)
        return pos
    
            
    def finish_request(self, printMsg = False):
        
        self._finish = False     
        self.send_gcode("M114", wait_until_completion=False, printMsg=printMsg)
    
    def get_finish_flag(self):
        return self._finish
                        
        
class position:
    def __init__(self, x=None, y=None, z=None, e=None, f=None):
        self.x = x
        self.y = y
        self.z = z
        self.e = e
        self.f = f

import cv2

class VideoGear:
    def __init__(self, source, logging, **options):
        self.source = source
        self.options = {}
        for op in options:
            self.options[op] = options[op]
            
    
    def start(self):
        logger.debug(f"Starting video stream {self.source}")
        return self
        
    def read(self):
        if self.source == 0:
            return cv2.imread(r'Pictures\Utils\image14.png')
        else:
            return cv2.imread(r'Pictures\Utils\macro_image_0.png')
    
    def stop(self):
        logger.debug(f"Stopping video stream {self.source}")
        
