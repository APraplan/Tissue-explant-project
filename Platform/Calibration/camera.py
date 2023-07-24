import cv2
import numpy as np
import sys
sys.path.append('c:/Users/APrap/Documents/CREATE/Pick-and-Place/Platform')

import computer_vision as mcv
import pickle

detect_chessboard = False
detect_sample = False

num = 0

cap = cv2.VideoCapture(0) 
cap2 = cv2.VideoCapture(2)

cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FPS, 25)

cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap2.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap2.set(cv2.CAP_PROP_FPS, 25)

# Check if camera opened successfully
if not cap.isOpened():
    print("Error opening video stream or file")
    
    
ret, frame = cap.read() 

cam = mcv.Camera(frame)
frame = cam.undistort(frame)

mask = np.zeros(frame.shape[0:2], dtype='uint8')
center_coordinates = (int(mask.shape[1]/2), int(mask.shape[0]/2))
radius = 170
color = 255
thickness = -1
mask = cv2.circle(mask, center_coordinates, radius, color, thickness)

chessboardSize = (9, 6)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

printed = False
    
while(True): 

    # reads frames from a camera 
    _, frame = cap.read() 
    _, frame2 = cap2.read()
    frame = cam.undistort(frame)
    
    cv2.imshow('Camera', frame) 
    cv2.imshow('Macro cam', frame2)
       
    # Detection
    if detect_sample:
        out = mcv.detection_test(frame, mask)
        cv2.imshow('Detection', out)
    
    # # Detection chessboard
    if detect_chessboard:
        out = frame.copy()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, chessboardSize, None)
        if ret:
            corners = cv2.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
            out = cv2.drawChessboardCorners(out, chessboardSize, corners, ret)
        cv2.imshow('Chessboard', out)
    
    if not printed:
        print(frame.shape)
        printed = True

    # Wait for Esc key to stop 
    k = cv2.waitKeyEx(5)
    if k == ord('p'):
        # path = "C:\Users\APrap\Documents\CREATE\Pick-and-Place\Pictures\image" + str(num)
        cv2.imwrite(r"Pictures/Realsample/image" + str(num) + ".png", frame)
        num += 1
    
    if k == 27: 
        break
    
cap.release() 
cv2.destroyAllWindows()


