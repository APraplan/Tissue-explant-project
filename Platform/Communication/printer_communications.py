import serial
from threading import Thread
from time import time, sleep
import sys

class printer:
    def __init__(self, descriptive_device_name, port_name, baudrate):
        # Communication inputs
        self.descriptive_device_name = descriptive_device_name
        self.port_name = port_name
        self.baudrate = baudrate

        # Communication
        self._raw_received_message = None
        self.printer = None
        self._ok_flag = False

        # Other
        self.home_pos = [0,0,0]
        self._finish = False

    def _serial_readline(self):
        while True:
            try:
                self._raw_received_message = self.printer.readline().decode('utf-8')[:-1]
                if self._raw_received_message == "ok":
                    self._ok_flag = True
                if self._raw_received_message[:1] == "X":
                    self._finish = True
            except:
                pass
            sleep(0.001)

    def _start_Reading_Thread(self):
        self.__thread = Thread(target=self._serial_readline)
        self.__thread.daemon = True
        self.__thread.start()

    def connect(self, timeout = 20):
        try: 
            self.printer = serial.Serial(port=self.port_name, baudrate=self.baudrate)
            print("Successfully connected to " + self.descriptive_device_name)
        except:
            print("!! Cannot connect to " + self.descriptive_device_name + " !!")
            sys.exit()

        self._start_Reading_Thread()

        print("Waiting until printer initializes")
        timer = time()
        while True:
            if self._raw_received_message == "echo:SD init fail":
                print("Successfully initialized " + self.descriptive_device_name)
                break

            if time() - timer > timeout:
                print("!! " +  self.descriptive_device_name + " init failed !!")
                sys.exit()

    def disconnect(self):
        try: 
            self.printer.close()
            print("Disconnected " + self.descriptive_device_name)
        except:
            print("!! Cannot disconnect " + self.descriptive_device_name + " !!")
            sys.exit()

    def _send_msg(self, msg):
        self.printer.write(str.encode(msg)) 

    def send_gcode(self, gcode, wait_until_completion = True, printMsg = True):
        self._ok_flag = False
        self._send_msg(gcode + "\r\n")

        if wait_until_completion:
            while True:
                if self._ok_flag: 
                    break
            if printMsg:
                print("Process complete: ", gcode)

    def max_x_feedrate(self, speed):
        self.send_gcode("M203 X" + str(float(speed)), printMsg=False)

    def max_y_feedrate(self, speed):
        self.send_gcode("M203 Y" + str(float(speed)), printMsg=False)
        
    def max_z_feedrate(self, speed):
        self.send_gcode("M203 Z" + str(float(speed)), printMsg=False)

    def stop_motion(self):
        self.send_gcode("M410", printMsg=False)

    def set_home_pos(self, x = 0, y = 0, z = 0):
        self.home_pos = [x, y, z]

    def homing(self, printMsg=False):
        self.send_gcode("G28 R25", printMsg=printMsg)
        
    def move_speed(self, speed):
        self.send_gcode("M203 X" + str(float(speed)) + " Y" + str(float(speed)) + " Z" + str(float(speed)), printMsg=False)

    def move_home(self, f = 1000, printMsg=False):
        self.move_axis(x = self.home_pos[0], y = self.home_pos[1], z = self.home_pos[2], f = f, printMsg=printMsg)

    def move_axis_relative(self, x = None, y = None, z = None, e = None, f = None, printMsg = False):
        self._finish = False
        command = "G0"
        
        if x is not None:
            command = command + " X" + str(x + self.home_pos[0])
        if y is not None:
            command = command + " Y" + str(y + self.home_pos[1])
        if z is not None:
            command = command + " Z" + str(z + self.home_pos[2])
        if e is not None:
            command = command + " E" + str(e)
        if f is not None:
            command = command + " F" + str(float(f))

        self.send_gcode(command, wait_until_completion=True, printMsg=printMsg)

    def move_axis(self, x = None, y = None, z = None, e = None, f = None, printMsg = False):
        self._finish = False
        command = "G0"
        
        if x is not None:
            command = command + " X" + str(x)
        if y is not None:
            command = command + " Y" + str(y)
        if z is not None:
            command = command + " Z" + str(z)
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
        if y is not None:
            command = command + " Y" + str(y + position[1])
        if z is not None:
            command = command + " Z" + str(z + position[2])
        if e is not None:
            command = command + " E" + str(e)
        if f is not None:
            command = command + " F" + str(float(f))

        self.send_gcode(command, wait_until_completion=True, printMsg=printMsg)

    def read_position(self, printMsg=False):
        while True: 
            try:
                self.send_gcode("M114", wait_until_completion=False, printMsg=printMsg)

                pos = None
                while True:
                    if self._raw_received_message[:1] == "X" and pos is None:
                        pos = self._raw_received_message

                    if self._ok_flag: 
                        break
                
                if printMsg:
                    print("position:", pos)

                msg = pos.split(":")

                position = []
                for i, m in enumerate(msg):
                    if i > 0 and i < 4:
                        position.append(float(m[:-2]))

                return position
            except:
                # print('read position error')
                sleep(0.2)
                
                
    def read_position_relative(self, printMsg=False):
        pos = self.read_position()
        pos[0] = pos[0] + self.home_pos[0]
        pos[1] = pos[1] + self.home_pos[1]
        pos[2] = pos[2] + self.home_pos[2]
        
        if printMsg:
            print("position:", pos)
        return pos
    
            
    def finish_request(self, printMsg = False):
        
        self._finish = False     
        self.send_gcode("M114", wait_until_completion=False, printMsg=printMsg)
        
    def get_ok_flag(self):
        return self._ok_flag
    
    def get_finish_flag(self):
        return self._finish
                        
        
class position:
    def __init__(self, x=None, y=None, z=None, e=None, f=None):
        self.x = x
        self.y = y
        self.z = z
        self.e = e
        self.f = f
