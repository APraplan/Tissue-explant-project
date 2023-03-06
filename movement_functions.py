from printer_communications import *
from platform_lib import *
from geometric_functions import *
from helpers_pump import *
from comms_wrapper import *
import keyboard
sys.path.append('../')

anycubic = printer(descriptive_device_name="printer", port_name="COM10", baudrate=115200)
arduino = Arduino(descriptiveDeviceName='Arduino_pump', portName='COM14', baudrate=115200)

def platform_init():
    
    # Home position for the printer
    anycubic.connect()
    anycubic.homing()
    anycubic.set_home_pos(x=0, y=200, z=0)
    anycubic.max_x_feedrate(15000)
    anycubic.max_y_feedrate(15000)
    anycubic.max_z_feedrate(100)
    anycubic.move_home()
    
    arduino.connect_and_handshake()
    
def pick(object):
    
    # Calculate and move to an intermediate safe point 
    pos = anycubic.read_position()
    if(pos[2]<petri.z):
        safe_point = intermediate_point_cylinder(pos[0], pos[1], object.x, object.y, petri.r, petri.z)

        anycubic.move_axis(x=safe_point[0], y=safe_point[1], z=safe_point[2], f=15000)
        # while safe_point[0] != anycubic.read_position()[0]:
        #     pass
    
    # Move on the object
    anycubic.move_axis(x=object.x, y=object.y, z=petri.z)
    # while object.x != anycubic.read_position()[0]:
    #     pass
    
    # Pick
    anycubic.move_axis(z=petri.pick_z)
    while petri.pick_z != anycubic.read_position()[2]:
        pass
    
    # pick function
    # Pump(-1, 1, 100, arduino)       
    
    anycubic.move_axis(z=petri.z)
    # while petri.z != anycubic.read_position()[2]:
    #     pass
    
    

def place(x, y):
    
    # Calculate and move to an intermediate safe point    
    pos = anycubic.read_position()
    safe_point = intermediate_point_plan(pos[0], pos[1], x, y, tube.min_x, tube.max_x, tube.min_y, tube.max_y, tube.z)

    
    anycubic.move_axis(x=safe_point[0], y=safe_point[1], z=safe_point[2], f=15000)
    # while safe_point[0] != anycubic.read_position()[0]:
    #     pass
    
    # Move on the emplacement
    anycubic.move_axis(x=x, y=y)
    # while x != anycubic.read_position()[0]:
    #     pass

    # Place
    anycubic.move_axis(z=tube.place_z)
    while tube.place_z != anycubic.read_position()[2]:
        pass
    
    # place function
    # Pump(1, 1, 100, arduino)     
    
    
    anycubic.move_axis(z=tube.z)
    # while tube.z != anycubic.read_position()[2]:
    #     pass


def take_picture():
    pass

def manual_control():
    
    print('Press "esc" to quit')
    
    incr = 5
     

    while True:
        
        # Quit
        if keyboard.is_pressed("esc"):
            while keyboard.is_pressed('esc'):
                pass
            break
        
        # Speed
        if keyboard.is_pressed("1"):
            incr = 1
            print('Increment set to ', incr, ' mm')
        
        if keyboard.is_pressed("2"):
            incr = 5
            print('Increment set to ', incr, ' mm')
            
        if keyboard.is_pressed("3"):
            incr = 10
            print('Increment set to ', incr, ' mm')
            
        if keyboard.is_pressed("4"):
            incr = 50
            print('Increment set to ', incr, ' mm')
        
        # Anycubic
        if keyboard.is_pressed('r'):
            anycubic.read_position(printMsg=True)
            while keyboard.is_pressed('r'):
                pass
              
        if keyboard.is_pressed('a'):
            anycubic.move_axis_incremental(x=-incr, printMsg=False)
            
        if keyboard.is_pressed('d'):
            anycubic.move_axis_incremental(x=incr, printMsg=False)
            
        if keyboard.is_pressed('w'):
            anycubic.move_axis_incremental(y=-incr, printMsg=False)
            
        if keyboard.is_pressed('s'):
            anycubic.move_axis_incremental(y=incr, printMsg=False)
            
        if keyboard.is_pressed('e'):
            anycubic.move_axis_incremental(z=incr, printMsg=False)
    
        if keyboard.is_pressed('c'):
            anycubic.move_axis_incremental(z=-incr, printMsg=False)
        
        sleep(0.02)

def disconnect_all():
    anycubic.disconnect()

    print('Goodbye ;)')
