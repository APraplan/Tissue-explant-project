# from geometric_functions import *
# from comms_wrapper import *
# from helpers_pump import *
# from printer_communications import *
# import keyboard


# l = np.array([10, 0, 10])
# l0 = np.array([0, 0, 0])
# n = np.array([10, 0, 0])
# p0 = np.array([50, 0, 0])

# int = intermediate_point_cylinder(10,0,20,0,5,7)


# print(int)

# print(int(19/4))

# arduino = Arduino(descriptiveDeviceName='Arduino_pump', portName='COM14', baudrate=100000)

# arduino.connect_and_handshake()
# arduino.debug()

# # Pump(-1, 1, 100, arduino)

# import serial
# import time

# arduino = serial.Serial(port='COM14', baudrate=115200, timeout=.1)

# def write_read(x):
#     arduino.write(bytes(x, 'utf-8'))
#     time.sleep(0.05)
#     data = arduino.readline()
#     return data

# while True:
#     num = input("Enter a number: ") # Taking input from user
#     value = write_read(num)
#     print(value) # printing the value

















import cv2
import numpy as np
import Platform.computer_vision as mcv

def make_720p():
    cap.set(3, 1280)
    cap.set(4, 720)
    
def make_1080p():
    cap.set(3, 1920)
    cap.set(4, 1080)

num = 0

cap = cv2.VideoCapture(0) 

make_1080p()

# Check if camera opened successfully
if not cap.isOpened():
    print("Error opening video stream or file")
    
ret, frame = cap.read() 

mask = np.zeros(frame.shape[0:2], dtype='uint8')
center_coordinates = (int(mask.shape[1]/2), int(mask.shape[0]/2))
radius = 170
color = 255
thickness = -1
mask = cv2.circle(mask, center_coordinates, radius, color, thickness)

chessboardSize = (9, 6)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    
while(True): 

    # reads frames from a camera 
    _, frame = cap.read() 
    
    
    # Detection
    # out = mcv.detection_test(frame, mask)
    
    # Detection chessboard
    # out2 = frame.copy()
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Find the chess board corners
    # ret, corners = cv2.findChessboardCorners(gray, chessboardSize, None)
    
    # Display an original image 
    cv2.imshow('Camera', frame) 
    # cv2.imshow('Detection', out)
     
    # if ret is True:
    #     corners = cv2.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
    #     out2 = cv2.drawChessboardCorners(out2, chessboardSize, corners, ret)
    #     cv2.imshow('Chessboard', out2)

    # Wait for Esc key to stop 
    k = cv2.waitKey(5) & 0xFF
    if k == ord('p'):
        # path = "C:\Users\APrap\Documents\CREATE\Pick-and-Place\Pictures\image" + str(num)
        cv2.imwrite("Pictures\calibration\image" + str(num) + ".png", frame)
        num += 1
        pass
    
    if k == 27: 
        break
    
cap.release() 
cv2.destroyAllWindows()
















# anycubic = printer(descriptive_device_name="printer", port_name="COM10", baudrate=115200)

# anycubic.connect()
# anycubic.homing()
# anycubic.set_home_pos(x=0, y=200, z=0)
# anycubic.max_x_feedrate(15000)
# anycubic.max_y_feedrate(15000)
# anycubic.max_z_feedrate(100)
# # anycubic.move_home()


# path = []

# path.append(position(50, 50, 20, 0, 5000))
# path.append(position(150, 50, 25, 0, 5000))
# path.append(position(150, 150, 30, 0, 5000))
# path.append(position(50, 150, 35, 0, 5000))
# path.append(position(50, 50, 40, 0, 5000))
# path.append(position(150, 50, 45, 0, 5000))
# path.append(position(150, 150, 20, 0, 5000))


# print('Ready')
# keyboard.wait('enter')

# for i in range(len(path)):
    
#     position = path[i]
    
#     anycubic.move_axis(x=path[i].x, y=path[i].y, z=path[i].z, e=path[i].e, f=path[i].f)
#     while(anycubic.read_position()[0] != position.x and anycubic.read_position()
#           [1] != position.y):
#         pass
#     # command = "G0"
    
#     # if position.x is not None:
#     #     command = command + " X" + str
#     # (position.x)
#     # if position.y is not None:
#     #     command = command + " Y" + str(position.y)
#     # if position.z is not None:
#     #     command = command + " Z" + str(position.z)
#     # if position.e is not None:
#     #     command = command + " E" + str(position.e)
#     # if position.f is not None:
#     #     command = command + " F" + str(float(position.f))
            
#     # self.send_gcode(command, wait_until_completion=True, printMsg=printMsg)

# while True:
#     if keyboard.on_press('esc'):
#         break

