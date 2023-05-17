import sys
from dynamixel_sdk import * 
from Platform.Communication.dynamixel_address_book import *
import math

PIPETTE_MIN = [360, 3770]
PIPETTE_MAX = [2880, 1250]
TIP_POSITION = [3072, 2560, 3584]

class Dynamixel:
    def __init__(self, ID, descriptive_device_name, port_name, baudrate, series_name = "xm"):
        # Communication inputs
        if type(ID) == list:
            self.multiple_motors = True
        else:
            self.multiple_motors = False

        self.ID = ID
        self.descriptive_device_name = descriptive_device_name
        self.port_name = port_name
        self.baudrate = baudrate
        
        # Set series name
        if type(self.ID) == list:
            if type(series_name) == list and len(series_name) == len(self.ID):
                self.series_name = {}
                for i in range(len(self.ID)):
                    self.series_name[self.ID[i]] = series_name[i]
            else:
                print("Provide correct series name type / length")
                sys.exit()

        else:
            if type(series_name) == str:
                self.series_name = {self.ID: series_name}
            else:
                print("Provide correct series name type")

        for id, series in self.series_name.items():
            # Check for series name
            all_series_names = ["xm", "xl"]
            if series not in all_series_names:
                print("Series name invalid for motor with ID,", id, "Choose one of:", all_series_names)
                sys.exit()

        # Communication settings
        self.port_handler = PortHandler(self.port_name)
        self.packet_handler = PacketHandler(2)
        
        # pipette
        self.past_percentage = 0

    def fetch_and_check_ID(self, ID):
        if self.multiple_motors:
            if ID is None:
                print("You specified multiple dynamixels on this port. But did not specify which motor to operate upon. Please specify ID.")
                sys.exit()
            elif ID == "all":
                return self.ID
            elif type(ID) == list:
                for id in ID:
                    if id not in self.ID:
                        print("The ID you specified:", id, "in the list", ID, "does not exist in the list of IDs you initialized.")
                        sys.exit()
                return ID
            else:
                if ID in self.ID:
                    return [ID]
                else:
                    print("The ID you specified:", ID, "does not exist in the list of IDs you initialized.")
                    sys.exit()
        else:
            return [self.ID]

    def begin_communication(self, enable_torque = True):
        # Open port
        try: 
            self.port_handler.openPort()
            print("Port open successfully for:", self.descriptive_device_name)
        except:
            print("!! Failed to open port for:", self.descriptive_device_name)
            print("Check: \n1. If correct port name is specified\n2. If dynamixel wizard isn't connected")
            sys.exit()

        # Set port baudrate
        try:
            self.port_handler.setBaudRate(self.baudrate)
            print("Baudrate set successfully for:", self.descriptive_device_name)
        except:
            print("!! Failed to set baudrate for:", self.descriptive_device_name)
            sys.exit()

        if enable_torque:
            if self.multiple_motors:
                for ID in self.ID:
                    self.enable_torque(ID = ID)
            else:
                self.enable_torque()

    def end_communication(self, disable_torque = True):
        if disable_torque:
            if self.multiple_motors:
                for ID in self.ID:
                    self.disable_torque(ID = ID)
            else:
                self.disable_torque()

        # Close port
        try: 
            self.port_handler.closePort()
            print("Port closed successfully for:", self.descriptive_device_name)
        except:
            print("!! Failed to close port for:", self.descriptive_device_name)
            sys.exit()

    def _print_error_msg(self, process_name, dxl_comm_result, dxl_error, selected_ID, print_only_if_error = False):
        if dxl_comm_result != COMM_SUCCESS:
            print("!!", process_name, "failed for:", self.descriptive_device_name)
            print("Communication error:", self.packet_handler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("!!", process_name, "failed for:", self.descriptive_device_name)
            print("Dynamixel error:", self.packet_handler.getRxPacketError(dxl_error))
        else:
            if not print_only_if_error:
                print(process_name, "successful for:", self.descriptive_device_name, "ID:", selected_ID)

    def enable_torque(self, print_only_if_error=False, ID = None):
        selected_IDs = self.fetch_and_check_ID(ID)
        for selected_ID in selected_IDs:
            dxl_comm_result, dxl_error = self.packet_handler.write1ByteTxRx(self.port_handler, selected_ID, ADDR_TORQUE_ENABLE, 1)
            self._print_error_msg("Torque enable", dxl_comm_result=dxl_comm_result, dxl_error=dxl_error, selected_ID=selected_ID, print_only_if_error=print_only_if_error)

    def disable_torque(self, print_only_if_error=False, ID = None):
        selected_IDs = self.fetch_and_check_ID(ID)
        for selected_ID in selected_IDs:
            dxl_comm_result, dxl_error = self.packet_handler.write1ByteTxRx(self.port_handler, selected_ID, ADDR_TORQUE_ENABLE, 0)
            self._print_error_msg("Torque disable", dxl_comm_result=dxl_comm_result, dxl_error=dxl_error, selected_ID=selected_ID, print_only_if_error=print_only_if_error)
        
    def is_torque_on(self, print_only_if_error=False, ID = None):
        selected_IDs = self.fetch_and_check_ID(ID)
        for selected_ID in selected_IDs:
            torque_status, dxl_comm_result, dxl_error = self.packet_handler.read1ByteTxRx(self.port_handler, selected_ID, ADDR_TORQUE_ENABLE)
            self._print_error_msg("Read torque status", dxl_comm_result=dxl_comm_result, dxl_error=dxl_error, selected_ID=selected_ID, print_only_if_error=print_only_if_error)
            
            if torque_status == False:
                return False

        return True

    def ping(self, ID = None):
        selected_IDs = self.fetch_and_check_ID(ID)
        for selected_ID in selected_IDs:
            _, dxl_comm_result, dxl_error = self.packet_handler.ping(self.port_handler, selected_ID)
            self._print_error_msg("Ping", dxl_comm_result=dxl_comm_result, dxl_error=dxl_error, selected_ID=selected_ID)

    def set_operating_mode(self, mode, ID = None, print_only_if_error = False):
        selected_IDs = self.fetch_and_check_ID(ID)
        for selected_ID in selected_IDs:

            series = self.series_name[selected_ID]
            if series == "xm": 
                operating_modes = operating_modes_xm
            elif series == "xl":
                operating_modes = operating_modes_xl

            if mode in operating_modes:
                # Check if torque was enabled
                was_torque_on = False
                if self.is_torque_on(print_only_if_error = True, ID = selected_ID):
                    was_torque_on = True
                    self.disable_torque(print_only_if_error = True, ID = selected_ID)

                mode_id = operating_modes[mode]
                dxl_comm_result, dxl_error = self.packet_handler.write1ByteTxRx(self.port_handler, selected_ID, ADDR_OPERATING_MODE, mode_id)
                self._print_error_msg("Mode set to " + mode + " control", dxl_comm_result=dxl_comm_result, 
                                        dxl_error=dxl_error, selected_ID=selected_ID, print_only_if_error=print_only_if_error)

                if was_torque_on:
                    self.enable_torque(print_only_if_error=True, ID = selected_ID)
            else:
                print("Enter valid operating mode. Select one of:\n" + str(list(operating_modes.keys())))
                
    def set_velocity_gains(self,  P_gain = None, I_gain = None, ID = None):
        selected_IDs = self.fetch_and_check_ID(ID)
        for selected_ID in selected_IDs:
            if P_gain is not None:
                dxl_comm_result, dxl_error = self.packet_handler.write2ByteTxRx(self.port_handler, selected_ID, ADDR_VELOCITY_P_GAIN, int(P_gain))
                self._print_error_msg("Write velocity P gain", dxl_comm_result=dxl_comm_result, dxl_error=dxl_error, selected_ID=selected_ID, print_only_if_error=True)
            
            if I_gain is not None:
                dxl_comm_result, dxl_error = self.packet_handler.write2ByteTxRx(self.port_handler, selected_ID, ADDR_VELOCITY_I_GAIN, int(I_gain))
                self._print_error_msg("Write velocity I gain", dxl_comm_result=dxl_comm_result, dxl_error=dxl_error, selected_ID=selected_ID, print_only_if_error=True)

    def set_position_gains(self, P_gain = None, I_gain = None, D_gain = None, ID = None):
        selected_IDs = self.fetch_and_check_ID(ID)
        for selected_ID in selected_IDs:
            if P_gain is not None:
                dxl_comm_result, dxl_error = self.packet_handler.write2ByteTxRx(self.port_handler, selected_ID, ADDR_POSITION_P_GAIN, int(P_gain))
                self._print_error_msg("Write position P gain", dxl_comm_result=dxl_comm_result, dxl_error=dxl_error, selected_ID=selected_ID, print_only_if_error=True)
            
            if I_gain is not None:
                dxl_comm_result, dxl_error = self.packet_handler.write2ByteTxRx(self.port_handler, selected_ID, ADDR_POSITION_I_GAIN, int(I_gain))
                self._print_error_msg("Write position I gain", dxl_comm_result=dxl_comm_result, dxl_error=dxl_error, selected_ID=selected_ID, print_only_if_error=True)

            if D_gain is not None:
                dxl_comm_result, dxl_error = self.packet_handler.write2ByteTxRx(self.port_handler, selected_ID, ADDR_POSITION_D_GAIN, int(D_gain))
                self._print_error_msg("Write position D gain", dxl_comm_result=dxl_comm_result, dxl_error=dxl_error, selected_ID=selected_ID, print_only_if_error=True)
                
    def compensate_twos_complement(self, value, quantity):
        if quantity in max_register_value:
            max_value = max_register_value[quantity]

            if value < max_value/2:
                return value
            else:
                return value - max_value
        else:
            print("Enter valid operating mode. Select one of:\n" + str(list(max_register_value.keys())))

    def read_position(self, ID = None):
        selected_IDs = self.fetch_and_check_ID(ID)
        reading = []
        for selected_ID in selected_IDs:
            position, dxl_comm_result, dxl_error = self.packet_handler.read4ByteTxRx(self.port_handler, selected_ID, ADDR_PRESENT_POSITION)
            self._print_error_msg("Read position", dxl_comm_result=dxl_comm_result, dxl_error=dxl_error, selected_ID=selected_ID, print_only_if_error=True)
            reading.append(self.compensate_twos_complement(position, "position"))
            
        if len(selected_IDs) == 1:
            return reading[0]
        else:
            return reading
            
    def read_velocity(self, ID = None):
        selected_IDs = self.fetch_and_check_ID(ID)
        reading = []
        for selected_ID in selected_IDs:
            velocity, dxl_comm_result, dxl_error = self.packet_handler.read4ByteTxRx(self.port_handler, selected_ID, ADDR_PRESENT_VELOCITY)
            self._print_error_msg("Read velocity", dxl_comm_result=dxl_comm_result, dxl_error=dxl_error, selected_ID=selected_ID, print_only_if_error=True)
            reading.append(self.compensate_twos_complement(velocity, "velocity"))
        
        if len(selected_IDs) == 1:
            return reading[0]
        else:
            return reading

    def read_current(self, ID = None):
        selected_IDs = self.fetch_and_check_ID(ID)
        reading = []
        for selected_ID in selected_IDs:
            current, dxl_comm_result, dxl_error = self.packet_handler.read2ByteTxRx(self.port_handler, selected_ID, ADDR_PRESENT_CURRENT)
            self._print_error_msg("Read cuurent", dxl_comm_result=dxl_comm_result, dxl_error=dxl_error, selected_ID=selected_ID, print_only_if_error=True)
            reading.append(self.compensate_twos_complement(current, "current"))

        if len(selected_IDs) == 1:
            return reading[0]
        else:
            return reading

    def read_pwm(self, ID = None):
        selected_IDs = self.fetch_and_check_ID(ID)
        reading = []
        for selected_ID in selected_IDs:
            pwm, dxl_comm_result, dxl_error = self.packet_handler.read2ByteTxRx(self.port_handler, selected_ID, ADDR_PRESENT_PWM)
            self._print_error_msg("Read pwm", dxl_comm_result=dxl_comm_result, dxl_error=dxl_error, selected_ID=selected_ID, print_only_if_error=True)
            reading.append(self.compensate_twos_complement(pwm, "pwm"))

        if len(selected_IDs) == 1:
            return reading[0]
        else:
            return reading

    def read_from_address(self, number_of_bytes, ADDR, ID = None):
        selected_IDs = self.fetch_and_check_ID(ID)
        reading = []
        for selected_ID in selected_IDs:

            twos_complement_key = ""
            if number_of_bytes == 1:
                value, dxl_comm_result, dxl_error = self.packet_handler.read1ByteTxRx(self.port_handler, selected_ID, ADDR)
                twos_complement_key = "1 byte"
            elif number_of_bytes == 2:
                value, dxl_comm_result, dxl_error = self.packet_handler.read2ByteTxRx(self.port_handler, selected_ID, ADDR)
                twos_complement_key = "2 bytes"
            else:
                value, dxl_comm_result, dxl_error = self.packet_handler.read4ByteTxRx(self.port_handler, selected_ID, ADDR)
                twos_complement_key = "4 bytes"

            self._print_error_msg("Read address", dxl_comm_result=dxl_comm_result, dxl_error=dxl_error, selected_ID=selected_ID, print_only_if_error=True)
            reading.append(self.compensate_twos_complement(value, twos_complement_key))
            
        if len(selected_IDs) == 1:
            return reading[0]
        else:
            return reading

    def write_position(self, pos, ID = None):
        selected_IDs = self.fetch_and_check_ID(ID)
        for selected_ID in selected_IDs:
            dxl_comm_result, dxl_error = self.packet_handler.write4ByteTxRx(self.port_handler, selected_ID, ADDR_GOAL_POSITION, int(pos))
            self._print_error_msg("Write position", dxl_comm_result=dxl_comm_result, dxl_error=dxl_error, selected_ID=selected_ID, print_only_if_error=True)

    def write_velocity(self, vel, ID = None):
        selected_IDs = self.fetch_and_check_ID(ID)
        for selected_ID in selected_IDs:
            dxl_comm_result, dxl_error = self.packet_handler.write4ByteTxRx(self.port_handler, selected_ID, ADDR_GOAL_VELOCITY, int(vel))
            self._print_error_msg("Write velocity", dxl_comm_result=dxl_comm_result, dxl_error=dxl_error, selected_ID=selected_ID, print_only_if_error=True)
        
    def write_current(self, current, ID = None):
        selected_IDs = self.fetch_and_check_ID(ID)
        for selected_ID in selected_IDs:
            dxl_comm_result, dxl_error = self.packet_handler.write2ByteTxRx(self.port_handler, selected_ID, ADDR_GOAL_CURRENT, int(current))
            self._print_error_msg("Write current", dxl_comm_result=dxl_comm_result, dxl_error=dxl_error, selected_ID=selected_ID, print_only_if_error=True)
    
    def write_pwm(self, pwm, ID = None):
        selected_IDs = self.fetch_and_check_ID(ID)
        for selected_ID in selected_IDs:
            dxl_comm_result, dxl_error = self.packet_handler.write2ByteTxRx(self.port_handler, selected_ID, ADDR_GOAL_PWM, int(pwm))
            self._print_error_msg("Write pwm", dxl_comm_result=dxl_comm_result, dxl_error=dxl_error, selected_ID=selected_ID, print_only_if_error=True)

    def write_profile_velocity(self, profile_vel, ID = None):
        selected_IDs = self.fetch_and_check_ID(ID)
        for selected_ID in selected_IDs:
            dxl_comm_result, dxl_error = self.packet_handler.write4ByteTxRx(self.port_handler, selected_ID, ADDR_PROFILE_VELOCITY, int(profile_vel))
            self._print_error_msg("Write profile velocity", dxl_comm_result=dxl_comm_result, dxl_error=dxl_error, selected_ID=selected_ID, print_only_if_error=True)
        
    def write_profile_acceleration(self, profile_acc, ID = None):
        selected_IDs = self.fetch_and_check_ID(ID)
        for selected_ID in selected_IDs:
            dxl_comm_result, dxl_error = self.packet_handler.write4ByteTxRx(self.port_handler, selected_ID, ADDR_PROFILE_ACCELERATION, int(profile_acc))
            self._print_error_msg("Write profile acceleration", dxl_comm_result=dxl_comm_result, dxl_error=dxl_error, selected_ID=selected_ID, print_only_if_error=True)
        
    def write_to_address(self, value, number_of_bytes, ADDR, ID = None):
        selected_IDs = self.fetch_and_check_ID(ID)
        for selected_ID in selected_IDs:

            if number_of_bytes == 1: 
                dxl_comm_result, dxl_error = self.packet_handler.write1ByteTxRx(self.port_handler, selected_ID, ADDR, int(value))
            elif number_of_bytes == 2: 
                dxl_comm_result, dxl_error = self.packet_handler.write2ByteTxRx(self.port_handler, selected_ID, ADDR, int(value))
            else: 
                dxl_comm_result, dxl_error = self.packet_handler.write4ByteTxRx(self.port_handler, selected_ID, ADDR, int(value))
                    
            self._print_error_msg("Write to address", dxl_comm_result=dxl_comm_result, dxl_error=dxl_error, selected_ID=selected_ID, print_only_if_error=True)
         
    
    def write_pipette(self, percentage, ID = None):
            
        if percentage > 100:
            percentage = 100
        elif percentage < 0:
            percentage = 0
            
        selected_IDs = self.fetch_and_check_ID(ID)
        for selected_ID in selected_IDs:
            pos = int(PIPETTE_MIN[selected_ID-1] + percentage/100.0*(PIPETTE_MAX[selected_ID-1]-PIPETTE_MIN[selected_ID-1]))
            self.write_position(pos=pos, ID = selected_ID)
            
            
    def pipette_is_in_position(self, percentage, ID = None):
        
        d_pos = int(PIPETTE_MIN[ID-1] + percentage/100.0*(PIPETTE_MAX[ID-1]-PIPETTE_MIN[ID-1]))
        
        a_pos = self.read_position(ID = ID)
        
        if abs(d_pos-a_pos) <= 2:
            return True
        else:
            return False
        
    def select_tip(self, tip_number, ID = None):
        selected_IDs = self.fetch_and_check_ID(ID)
        for selected_ID in selected_IDs:
            self.write_position(pos=TIP_POSITION[tip_number], ID = selected_ID)      
        