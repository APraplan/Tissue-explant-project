from printer_communications import *
from platform_lib import *
from geometric_functions import *
from helpers_pump import *
from dynamixel_controller import *
import keyboard
import computer_vision as cv
import cv2
sys.path.append('../')

anycubic = printer(descriptive_device_name="printer", port_name="COM4", baudrate=115200)
dyna = Dynamixel(ID=[1], descriptive_device_name="XL430 test motor", series_name=["xl"], baudrate=57600,
                 port_name="COM12")
detector = cv.create_detector()
platform = platform_pick_and_place(anycubic=anycubic, dynamixel=dyna, detector=detector)

def platform_init():
    
    # Home position for the printer
    anycubic.connect()
    anycubic.homing()
    anycubic.set_home_pos(x=0, y=200, z=0)
    # anycubic.max_x_feedrate(15000)
    # anycubic.max_y_feedrate(15000)
    # anycubic.max_z_feedrate(100)
    # anycubic.move_home()
    
    dyna.begin_communication()
    dyna.set_operating_mode("position", ID=1)
    dyna.write_position(dyna.pipette(0), ID=1)
    
# def pick(object):
    
#     if platform.state[1] == 'empty pipette':
        
#     # if platform.state[2] == 'not send':
#     #     dyna.write_profile_velocity(platform.pipette_empty_speed, ID = 1)
#     #     dyna.pipette(80, ID = 1)
#     #     platform.state[2] = 'send'
        
#     # elif dyna.
    
#     # Calculate and move to an intermediate safe point 
#     pos = anycubic.read_position()
#     if(pos[2]<petri.z):
#         safe_point = intermediate_point_cylinder(pos[0], pos[1], object.x, object.y, petri.r, petri.z)

#         anycubic.move_axis_relative(x=safe_point[0], y=safe_point[1], z=safe_point[2], f=FEEDRATE)
#         # while safe_point[0] != anycubic.read_position()[0]:
#         #     pass
    
#     # Move on the object
#     anycubic.move_axis_relative(x=object.x, y=object.y, z=petri.z)
#     # while object.x != anycubic.read_position()[0]:
#     #     pass
    
#     # Pick
#     anycubic.move_axis_relative(z=petri.pick_z)
#     while petri.pick_z != anycubic.read_position()[2]:
#         pass
    
#     # pick function
#     # Pump(-1, 1, 100, arduino)       
    
#     anycubic.move_axis_relative(z=petri.z)
#     # while petri.z != anycubic.read_position()[2]:
#     #     pass    
    

# def place(x, y):
    
#     # Calculate and move to an intermediate safe point    
#     pos = anycubic.read_position()
#     safe_point = intermediate_point_plan(pos[0], pos[1], x, y, tube.min_x, tube.max_x, tube.min_y, tube.max_y, tube.z)

    
#     anycubic.move_axis_relative(x=safe_point[0], y=safe_point[1], z=safe_point[2], f=FEEDRATE)
#     # while safe_point[0] != anycubic.read_position()[0]:
#     #     pass
    
#     # Move on the emplacement
#     anycubic.move_axis_relative(x=x, y=y)
#     # while x != anycubic.read_position()[0]:
#     #     pass

#     # Place
#     anycubic.move_axis_relative(z=tube.place_z)
#     while tube.place_z != anycubic.read_position()[2]:
#         pass
    
#     # place function
#     # Pump(1, 1, 100, arduino)     
    
    
#     anycubic.move_axis_relative(z=tube.z)
#     # while tube.z != anycubic.read_position()[2]:
#     #     pass


# def take_picture():
    
#     if platform.state[1] == 'go up secutity':
        
#         if platform.state[2] == 'not send':
#             anycubic.move_axis(z=platform.safe_height, f=platform.speed_fast)
#             platform.state[2] = 'send'
            
#         elif platform.safe_height == anycubic.read_position()[2]:
#             platform.state[1] = 'go to detection place'
#             platform.state[2] = 'not send'
            
            
    # if platform.state[1] == 'go to detection place':
        
    #     if platform.state[2] == 'not send':
    #         anycubic.move_axis(x=platform.detection_place[0], y=platform.detection_place[1], z=platform.detection_place[2], f=platform.speed_fast)
    #         platform.state[2] = 'send'
            
    #     elif platform.detection_place[0] == anycubic.read_position()[0]:
    #         platform.state[1] = 'analyse picture'
    #         platform.state[2] = 'not send'
            
            
    # if platform.state[1] == 'analyse picture':
        
    #     # detection_tissue(frame)
    #     platform.state[1] = 'analyse picture'
    #     platform.state[2] = 'not send'
        
    #     ## fonciton de detection si pas trouvé recommance au bout de 30 essais quitte 
    #     platform.state[0] = 'pick'

        
        

# def manual_control():
    
#     print('Press "esc" to quit')
    
#     incr = 5
     

#     while True:
        
#         # Quit
#         if keyboard.is_pressed("esc"):
#             while keyboard.is_pressed('esc'):
#                 pass
#             break
        
#         # Speed
#         if keyboard.is_pressed("1"):
#             incr = 0.1
#             print('Increment set to ', incr, ' mm')
        
#         if keyboard.is_pressed("2"):
#             incr = 5
#             print('Increment set to ', incr, ' mm')
            
#         if keyboard.is_pressed("3"):
#             incr = 10
#             print('Increment set to ', incr, ' mm')
            
#         if keyboard.is_pressed("4"):
#             incr = 50
#             print('Increment set to ', incr, ' mm')
        
#         # Anycubic
#         if keyboard.is_pressed('r'):
#             anycubic.read_position_relative(printMsg=True)
#             while keyboard.is_pressed('r'):
#                 pass
              
#         if keyboard.is_pressed('a'):
#             anycubic.move_axis_incremental(x=-incr, printMsg=False)
            
#         if keyboard.is_pressed('d'):
#             anycubic.move_axis_incremental(x=incr, printMsg=False)
            
#         if keyboard.is_pressed('w'):
#             anycubic.move_axis_incremental(y=incr, printMsg=False)
            
#         if keyboard.is_pressed('s'):
#             anycubic.move_axis_incremental(y=-incr, printMsg=False)
            
#         if keyboard.is_pressed('e'):
#             anycubic.move_axis_incremental(z=incr, printMsg=False)
    
#         if keyboard.is_pressed('c'):
#             anycubic.move_axis_incremental(z=-incr, printMsg=False)
            
#         if keyboard.is_pressed('x'):
#             print('Home point set')
#             pos = anycubic.read_position(printMsg=False)
#             anycubic.set_home_pos(30-pos[0], 25-pos[1])
        
#         sleep(0.02)

def disconnect_all():
    
    anycubic.disconnect()
    dyna.end_communication()
    
    print('Goodbye ;)')

def manual_control():
    
    print('Press "esc" to quit')
    
    incr = 10
    
    cap = cv2.VideoCapture(0) 

    # Check if camera opened successfully
    if not cap.isOpened():
        print("Error opening video stream or file")
    
# ret, frame = cap.read() 

# mask = np.zeros(frame.shape[0:2], dtype='uint8')
# center_coordinates = (int(mask.shape[1]/2), int(mask.shape[0]/2))
# radius = 170
# color = 255
# thickness = -1
# mask = cv2.circle(mask, center_coordinates, radius, color, thickness)
    
    while(True): 

        # reads frames from a camera 
        _, frame = cap.read() 
        
        # Display an original image 
        cv2.imshow('Camera', frame) 

         # Wait for Esc key to stop 
        k = cv2.waitKey(5) & 0xFF
        if k == ord('p'):
            # path = "C:\Users\APrap\Documents\CREATE\Pick-and-Place\Pictures\image" + str(num)
            cv2.imwrite("Pictures/image" + str(num) + ".png", frame)
            num += 1
            pass
        
        incr = commande(k, incr)
        
    
        if k == 27: 
            break
    
    cap.release() 
    cv2.destroyAllWindows()
    
def commande(key, incr):
    
    # Speed
    if key == ord("1"):
        incr = 0.1
        print('Increment set to ', incr, ' mm')
    
    if key == ord("2"):
        incr = 5
        print('Increment set to ', incr, ' mm')
        
    if key == ord("3"):
        incr = 10
        print('Increment set to ', incr, ' mm')
        
    if key == ord("4"):
        incr = 50
        print('Increment set to ', incr, ' mm')
    
    # Anycubic
    if key == ord('r'):
        anycubic.read_position_relative(printMsg=True)
        while key == ord('r'):
            pass
        
    if key == ord('a'):
        anycubic.move_axis_incremental(x=-incr, printMsg=False)
        
    if key == ord('d'):
        anycubic.move_axis_incremental(x=incr, printMsg=False)
        
    if key == ord('w'):
        anycubic.move_axis_incremental(y=incr, printMsg=False)
        
    if key == ord('s'):
        anycubic.move_axis_incremental(y=-incr, printMsg=False)
        
    if key == ord('e'):
        anycubic.move_axis_incremental(z=incr, printMsg=False)

    if key == ord('c'):
        anycubic.move_axis_incremental(z=-incr, printMsg=False)
        
    if key == ord('8'):
        anycubic.move_axis(x = 100, y = 50, f = 3000)
    
    if key == ord('9'):
        anycubic.move_axis(x=50, y=50 ,f = 3000)
    
    if key == ord('0'):
        anycubic.move_axis(x=0, y=0, f = 3000)
        
    if key == ord('t'):
        anycubic.position_request()
    
        
    # if key == ord('x'):
    #     print('Home point set')
    #     pos = anycubic.read_position(printMsg=False)
    #     anycubic.set_home_pos(30-pos[0], 25-pos[1])
    
    return incr